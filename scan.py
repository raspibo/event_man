#!/usr/bin/python
import os
import pycurl
import ConfigParser
import zbar
from time import gmtime, strftime
import signal
import json

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    out_file.close()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
print 'Premi Ctrl+C per uscire'

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
                print("exception on %s!" % option)
                dict1[option] = None
    return dict1


def register_data(id):
    server = ConfigSectionMap("Server")
    action = ConfigSectionMap("Action")
    details = ConfigSectionMap("Details")
    event = ConfigSectionMap("Event")
    c = pycurl.Curl()
    register_code_url = server['protocol'] + '://' + server['address'] + ':' + server['port'] + '/events/' + event['id'] + '/persons/?ebqrcode=' + id 
    print register_code_url
    if server['protocol'] == "https":
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        #c.setopt(pycurl.SSL_VERIFYHOST, 2) # Use this line  for a production server
        c.setopt(pycurl.SSL_VERIFYHOST, 0)  # Use this to laboratory env
        if os.path.isfile(server['ca_cert_path']):
            c.setopt(pycurl.CAINFO, server['ca_cert_path'])

    c.setopt(c.URL, register_code_url)
    c.setopt(c.HTTPHEADER, [
        'Content-Type: application/json',
    ])
    #work from cli
    #curl -X PUT -H "Content-Type: application/json" -d '{"_id":"552591560025e836ebc92ed5","person_id":"5525907068ee09fee438fef5","attended":false}' http://lela.ismito.it:5242/events/552591560025e836ebc92ed5/persons/5525907068ee09fee438fef5
    date = strftime('%Y-%m-%dT%H:%M:%SZ',gmtime())
    put_data = json.dumps({"attended":True , "checkin_datetime": date});

    print put_data
    c.setopt(c.CUSTOMREQUEST, "PUT")

    # Form data must be provided already urlencoded.
    #postfields = urlencode(post_data)
    #print postfields
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    #c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.POSTFIELDS, put_data)

    c.perform()
    c.close()

    #out_file.write(id + ";" + action['direction'] + ";" + time.strftime('%Y-%m-%d %H:%M:%S') + ";" + details['operator'] + "\n")
    out_file.write( event['id'] + ";" + id + ";" + "True" + ";" + date  + "\n")

# setup a callback
def handle_webcam_lib(proc, image, closure):
    # extract results
        for symbol in image.symbols:
        # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

            id = symbol.data
            register_data(id)

Config = ConfigParser.ConfigParser()
Config.read("config.ini")
Config.sections()

out_file = open(ConfigSectionMap("Local")['logfile'],"a")

#print ConfigSectionMap("Input")['method']

if ConfigSectionMap("Input")['method'] == "webcam_lib":

    device = ConfigSectionMap("Input")['device']
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
        pass



if ConfigSectionMap("Input")['method'] == "webcam_os":
    device = ConfigSectionMap("Input")['device']
    #p = os.popen('LD_PRELOAD=/usr/lib/i386-linux-gnu/libv4l/v4l1compat.so zbarcam --raw /dev/video0','r')
    p = os.popen('/usr/bin/zbarcam ' + device ,'r')

    while True:
        code = p.readline()
        print 'BarCode/QrCode:', code
        id = code.split(':')[1]
        register_data(id[:-1])

if ConfigSectionMap("Input")['method'] == "manual" or ConfigSectionMap("Input")['method'] == "barcode_reader":
    while True:
        id = raw_input('Inserisci un valore: ')
        register_data(id)
