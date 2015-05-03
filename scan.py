#!/usr/bin/python
import os
import zbar
import logging
import requests
import ConfigParser
from time import gmtime, strftime
import signal


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    exit(0)


def config_options(section):
    dict1 = {}
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    config.sections()
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
                print("exception on %s!" % option)
                dict1[option] = None
    return dict1


def register_data(id_, session):
    server = config_options("Server")
    action = config_options("Action")
    details = config_options("Details")
    event = config_options("Event")
    register_code_url = '%s/events/%s/persons/?%s=%s' % (
            server['url'].rstrip('/'),
            event['id'],
            event['person_query_key'],
            id_)
    print register_code_url

    date = strftime('%Y-%m-%dT%H:%M:%SZ', gmtime())
    put_data = action['data'].replace('%NOW%', date).strip()
    print put_data
    session.put(register_code_url, data=put_data)
    logging.debug(event['id'] + ";" + id_ + ";" + "True" + ";" + date)


# setup a callback
def handle_webcam_lib(session, proc, image, closure):
        # extract results
        for symbol in image.symbols:
            # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
            id_ = symbol.data
            register_data(id_, session)


def run_webcam_lib(session):
    device = config_options("Input")['device']
    # create a Processor
    proc = zbar.Processor()
    # configure the Processor
    proc.parse_config('enable')
    proc.init(device)
    proc.set_data_handler(lambda *args: handle_webcam_lib(session, *args))
    # enable the preview window
    proc.visible = True
    # initiate scanning
    proc.active = True
    try:
        # keep scanning until user provides key/mouse input
        proc.user_wait()
    except zbar.WindowClosed, e:
        logging.info('window closed: %s' % e)


def run_webcam_os(session):
    device = config_options("Input")['device']
    p = os.popen('/usr/bin/zbarcam ' + device , 'r')
    while True:
        code = p.readline()
        print 'BarCode/QrCode:', code
        id_ = code.split(':')[1]
        register_data(id_[:-1], session)


def run_barcode(session):
    while True:
        id_ = raw_input('Inserisci un valore: ')
        register_data(id_, session)


def get_session():
    session = requests.Session()
    username = config_options('Server').get('username')
    password = config_options('Server').get('password')
    ca_cert = config_options('Server').get('ca_cert_path') or False
    url = config_options('Server')['url'] + '/v1.0'
    if username and password:
        response = session.post('%s/login' % url,
                data=dict(username=username, password=password),
                verify=ca_cert)
        if response.status_code != 200:
            logging.error('unable to authenticate or verify the host: %s' % response.text)
    else:
        response = session.get('%s/', verify=ca_cert)
        if response.status_code != 200:
            logging.error('unable to authenticate or verify the host: %s' % response.text)
    session.headers.update({'Content-type': 'application/json'})
    return session


def run():
    signal.signal(signal.SIGINT, signal_handler)
    print 'Premi Ctrl+C per uscire'
    session = get_session()
    if config_options("Input")['method'] == "webcam_lib":
        run_webcam_lib(session)
    elif config_options("Input")['method'] == "webcam_os":
        run_webcam_os(session)
    elif config_options("Input")['method'] == "manual" or config_options("Input")['method'] == "barcode_reader":
        run_barcode(session)

if __name__ == '__main__':
    run()

