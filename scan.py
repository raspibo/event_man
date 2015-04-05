#!/usr/bin/python

import os
import pycurl
import ConfigParser


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    Config.sections()

    device=ConfigSectionMap("Input")['device']

    p=os.popen('/usr/bin/zbarcam ' + device ,'r')
    #p=os.popen('LD_PRELOAD=/usr/lib/i386-linux-gnu/libv4l/v4l1compat.so zbarcam --raw /dev/video0','r')
    while True:
        code = p.readline()
        print 'Got BarCode/QrCode:', code
        id = code.split(':')[1]

        server=ConfigSectionMap("Server")
        action=ConfigSectionMap("Action")

        c = pycurl.Curl()
        register_code_url=server['protocol'] + '://' + server['address'] + ':' + server['port'] + '/' + server['url'] 
        print register_code_url
        c.setopt(c.URL, register_code_url)

        post_data = {'id': id , 'action' : action['direction'] }
        # Form data must be provided already urlencoded.
        postfields = urlencode(post_data)
	print postfields
        # Sets request method to POST,
        # Content-Type header to application/x-www-form-urlencoded
        # and data to send in request body.
        c.setopt(c.POSTFIELDS, postfields)

        c.perform()
        c.close()
