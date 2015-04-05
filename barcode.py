#!/usr/bin/python
#Simple barcode data logger 
#output on csv file
#usage: python barcode.py 
import time
import signal

def progTerm(signal,frame):
	print "\nterminando..."
	out_file.close()
	exit()

signal.signal(signal.SIGINT,progTerm)
out_file = open("log_accessi.csv","a")
print "I dati delle scansioni vengono visualizzati a video e salvati sul file log_accessi.csv"
print "Per terminare il programma usa Control+C"
print "Al momento la gestione delle operazioni si basa su input utente che indica manualmente se le letture riguardano entrata o uscita"
direzione=raw_input('Le letture sono per Entrata(E) o Uscita(U)?')
while 1:
        input = raw_input('Inserisci un valore: ')
        print time.strftime('%Y-%m-%d %H:%M:%S') + ";" + direzione + ";" + input
        out_file.write(time.strftime('%Y-%m-%d %H:%M:%S') + ";" + direzione + ";" + input + "\n")
