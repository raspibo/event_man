#!/usr/bin/python
import pdb
import os
import pycurl
import ConfigParser
from sys import argv
import zbar
import time 

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


def register_data(id):
	server=ConfigSectionMap("Server")
	action=ConfigSectionMap("Action")
	details=ConfigSectionMap("Details")

	c = pycurl.Curl()
	register_code_url=server['protocol'] + '://' + server['address'] + ':' + server['port'] + '/' + server['url'] 
	print register_code_url
	c.setopt(c.URL, register_code_url)

	post_data = {'id': id , 'action' : action['direction'], 'time' : time.strftime('%Y-%m-%d %H:%M:%S') , 'operator' : details['operator'] }
	# Form data must be provided already urlencoded.
	postfields = urlencode(post_data)
	print postfields
	# Sets request method to POST,
	# Content-Type header to application/x-www-form-urlencoded
	# and data to send in request body.
	c.setopt(c.POSTFIELDS, postfields)

	c.perform()
	c.close()

        #out_file.write(id + ";" + action['direction'] + ";" + time.strftime('%Y-%m-%d %H:%M:%S') + ";" + details['operator'] + "\n")
        out_file.write( id + ";" + action['direction'] + ";" + time.strftime('%Y-%m-%d %H:%M:%S') + ";" + details['operator'] + ";" + "\n")

# setup a callback
def handle_webcam_lib(proc, image, closure):
	# extract results
		for symbol in image.symbols:
		# do something useful with results
			print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

			id=symbol.data
			register_data(id)

Config = ConfigParser.ConfigParser()
Config.read("config.ini")
Config.sections()

out_file = open("log_accessi.csv","a")

#print ConfigSectionMap("Input")['method']

if ConfigSectionMap("Input")['method'] == "webcam_lib":

	device=ConfigSectionMap("Input")['device']
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
	device=ConfigSectionMap("Input")['device']
	#p=os.popen('LD_PRELOAD=/usr/lib/i386-linux-gnu/libv4l/v4l1compat.so zbarcam --raw /dev/video0','r')
    	p=os.popen('/usr/bin/zbarcam ' + device ,'r')

	while True:
		code = p.readline()
		print 'BarCode/QrCode:', code
		id = code.split(':')[1]
		register_data(id[:-1])

if ConfigSectionMap("Input")['method'] == "manual":
        id = raw_input('Inserisci un valore: ')
	register_data(id)
