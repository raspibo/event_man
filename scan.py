#!/usr/bin/python
import os
import pycurl
import logging
import ConfigParser
import zbar
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


def register_data(id_):
    server = config_options("Server")
    action = config_options("Action")
    details = config_options("Details")
    event = config_options("Event")
    c = pycurl.Curl()
    register_code_url = '%s/events/%s/persons/?%s=%s' % (
            server['url'].rstrip('/'),
            event['id'],
            event['person_query_key'],
            id_)
    print register_code_url
    if os.path.isfile(server['ca_cert_path']):
        c.setopt(pycurl.CAINFO, server['ca_cert_path'])
    else:
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)

    c.setopt(c.URL, register_code_url)
    c.setopt(c.HTTPHEADER, [
        'Content-Type: application/json',
    ])
    date = strftime('%Y-%m-%dT%H:%M:%SZ', gmtime())
    put_data = action['data'].replace('%NOW%', date).strip()
    print put_data
    c.setopt(c.CUSTOMREQUEST, "PUT")
    c.setopt(c.POSTFIELDS, put_data)
    c.perform()
    c.close()
    logging.debug(event['id'] + ";" + id_ + ";" + "True" + ";" + date)


# setup a callback
def handle_webcam_lib(proc, image, closure):
    # extract results
        for symbol in image.symbols:
            # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

            id_ = symbol.data
            register_data(id_)


def run_webcam_lib():
    device = config_options("Input")['device']
    # create a Processor
    proc = zbar.Processor()
    # configure the Processor
    proc.parse_config('enable')
    proc.init(device)
    proc.set_data_handler(handle_webcam_lib)
    # enable the preview window
    proc.visible = True
    # initiate scanning
    proc.active = True
    try:
        # keep scanning until user provides key/mouse input
        proc.user_wait()
    except zbar.WindowClosed, e:
        logging.info('window closed: %s' % e)


def run_webcam_os():
    device = config_options("Input")['device']
    p = os.popen('/usr/bin/zbarcam ' + device , 'r')
    while True:
        code = p.readline()
        print 'BarCode/QrCode:', code
        id_ = code.split(':')[1]
        register_data(id_[:-1])

def run_barcode():
    while True:
        id_ = raw_input('Inserisci un valore: ')
        register_data(id_)


def run():
    signal.signal(signal.SIGINT, signal_handler)
    print 'Premi Ctrl+C per uscire'
    if config_options("Input")['method'] == "webcam_lib":
        run_webcam_lib()
    elif config_options("Input")['method'] == "webcam_os":
        run_webcam_os()
    elif config_options("Input")['method'] == "manual" or config_options("Input")['method'] == "barcode_reader":
        run_barcode()

if __name__ == '__main__':
    run()

