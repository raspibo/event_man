#!/usr/bin/python
#Simple barcode data logger 
#output on csv file
#usage: python barcode.py 
import time
out_file = open("log_python.csv","w")
direzione=raw_input('Entrata o uscita?')
while 1:
        input = raw_input('Inserisci un valore: ')
        print time.strftime('%Y-%m-%d %H:%M:%S') + ";" + direzione + ";" + input
        out_file.write(time.strftime('%Y-%m-%d %H:%M:%S') + ";" + direzione + ";" + input + "\n")
out_file.close()

