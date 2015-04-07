#event_man
Simple event manager utilities specific for attendant registration, checkin, checkout trace.
All operations can be handled with barcode reader, webcam (as qrcode/barcode reader), keyboard.
#Config

Config file config.ini contain some parameters to define 

    [Input]
    Manual insert of id with keyboard
    Method: manual			
    Use barcode_reader to use barcode gun reader 
    Method: barcode_reader 	
    This method use zbarcam os command (require sudo apt-get install zbar-tools)
    Method: webcam_os		
    webcam_lib use puthon zbar module require sudo pip install zbar (optional? libzbar-dev)
    Method: webcam_lib
    Method webcam_* require video device
    Device: /dev/video0		
    [Server]
    Protocol: http
    Address: 192.168.1.115
    Port: 80
    Url: scan
    [Local]
    Local log file (in csv format)
    Logfile:log_accessi.csv
    [Event]
    Define event to handle
    Hackinbo20150523
    [Action]
    Track checkin or checkout with this parameter
    Direction: checkin
    Direction: checkout
    [Details]
    If you have multiple check point and you want to track single point assign a operator name
    Operator: eventman

Install procedure:
===========

    git clone https://github.com/raspibo/event_man/
    Check config.ini and run (if required)
    sudo apt-get install zbar-tools
    or 
    sudo pip install zbar

Start program with:

    python scan.py
Monitor Logfile and Server to track realtime data
