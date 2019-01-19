#!/usr/bin/python3
# encoding=utf-8

import time
import ConfigParser
import socket
import serial
import os
import threading
import logging
import signal
import sys

time.sleep(55) # warten bis raspberry fertig gestartet hat

def main():
	# ---------------------------------------------
	# Globale Variablen
	# ---------------------------------------------
	separator = ";"

#Systemvariable auslesen
lbpconfig = os.environ['LBPCONFIG']
lbsconfig = os.environ['LBSCONFIG']
lbplog = os.environ['LBPLOG']
# ---------------------------------------------
# Durchsuche PlugIn config file
# ---------------------------------------------
pluginconfig = ConfigParser.ConfigParser()
pluginconfig.read(lbpconfig + "/serialusb-bridge/serialusb-bridge-config.cfg")

enabled = pluginconfig.get('serialusbbridge-config', 'ENABLED')
miniservername = pluginconfig.get('serialusbbridge-config', 'MINISERVER')
virtualUDPPort = int(pluginconfig.get('serialusbbridge-config', 'UDPPORT'))
anschlussport4 = pluginconfig.get('serialusbbridge-config', 'USB4ID')
usbakt4 = pluginconfig.get('serialusbbridge-config', 'ENABLEDUSB4')
anschlussbaud4 = pluginconfig.get('serialusbbridge-config', 'USB4BAUD')
anschlussport = int(pluginconfig.get('serialusbbridge-config', 'USB4PORT'))
usb4praefix = pluginconfig.get('serialusbbridge-config', 'USB4PRAEFIX')

# ---------------------------------------------
# Durchsuche Loxberry config file für die Miniserverdaten
# ---------------------------------------------
loxberryconfig = ConfigParser.ConfigParser()
loxberryconfig.read(lbsconfig + "/general.cfg")
miniserverIP = loxberryconfig.get(miniservername, 'IPADDRESS')
loxberryIP = loxberryconfig.get('NETWORK', 'IPADDRESS')

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sockloxberryusb4 = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sockloxberryusb4.bind((loxberryIP, anschlussport)) 


# ---------------------------------------------
# Loglevelerkennung
# ---------------------------------------------
loglv = "WARNING" #standard loglevel
loglvint = int(pluginconfig.get('serialusbbridge-config', 'LOGLV'))
if loglvint == 10:
	loglv = "INFO"
if loglvint == 20:
	loglv = "WARNING"
if loglvint == 30:
	loglv = "ERROR"
	
# ---------------------------------------------
# Starteintrag in logdatei schreiben
# ---------------------------------------------	
zeit = time.strftime("%d.%m.%Y %H:%M:%S")

logging.basicConfig(filename= lbplog + '/serialusb-bridge/serialusb-bridge.log', filemode='a', level=loglv) #logging starten und die einträge anfügen
logging.warning(" Script von USB-4 neu Gestartet    " + zeit)

# ---------------------------------------------
# Exit wenn PlugIn nicht eingeschalten ist
# ---------------------------------------------
if enabled != "1":
	logging.info("SCRIPT USB4 BEENDET DA ES NICHT AKTIVIERT IST")
	sys.exit(-1)
if usbakt4 != "1":
	logging.info("SCRIPT USB4 BEENDET DA ADAPERT NICHT AKTIVIERT IST")
	sys.exit(-1)

# ---------------------------------------------
# Serielle Kommunikation
# ---------------------------------------------

s4 = serial.Serial(anschlussport4, anschlussbaud4)					 	#arduino nano Seriallellen Port öffnen

#prüfen ob port offen ist  ; 3 sec warten und nochmal prüfen 3x
i = 0
if s4.isOpen() == False and i <= 3:										
	ser.open()
	i += 1	
	time.sleep(3)
if s4.isOpen() == False and i == 4:					# wenn der port nicht geöffnet werden konnte logdatei schreiben
	logging.error("Script USB-4 Konnte USB Gerät nicht öffnen  :   " + zeit + "\n" + "ID: " + anschlussport4 + "    BAUD: " + anschlussbaud4 + "\n" + "\n")

def a():
		try:   											#überwachung ob fehler sind											#daten von Arduino Nano
			while True :
				data, addr = sockloxberryusb4.recvfrom(1024) 							# buffer ist 1024 bytes und wird von loxone empfangen
				data2 = data
				usberkennung = data2[0:6]  #erkennen ob usb 1,....
				usbdaten = data2[6:]		#usb-x= löschen
				if usberkennung == "USB-4=":	# wenn usb-2 vorgestellt ist die restlichen daten seriell schreiben
					s4.write(usbdaten) # daten seriell schreiben
					logging.info("DATENWEG USB4 OK UDP ->USB daten  :" + usbdaten)					
		except Exception as e:
			logging.exception("\n\n\n" + "Fehler bei Script USB-4 Von UDP zu Seriell     " + zeit)				#logeintrag schreiben
			for line in os.popen("ps ax | grep  serialusb-bridge-script-usb4.py | grep -v grep"):			# ganzes script mit threads killen
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)

def b():	
		try:   											#überwachung ob fehler sind
			while True :
					response = s4.readline() 				#Serielles lesen am usb (nano)
					response2 = usb4praefix + response					# kopie wird erstellt und mit der präfix befüllt
					sock.sendto(response2,(miniserverIP,virtualUDPPort)) 		#daten werden zu loxone gesendet     
					logging.info("DATENWEG USB4 OK USB -> UDP daten  :" + response2)
		except Exception as e:
			logging.exception("\n\n\n" + "Fehler bei Script USB-4 Von Seriell zu UDP  " + zeit)					#logeintrag schreiben
			for line in os.popen("ps ax | grep  serialusb-bridge-script-usb4.py | grep -v grep"):			# ganzes script mit threads killen
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)
				
#threading das gesendet und empfangen gleichzeit werden kann
udpreceiver = threading.Thread(target = a)		
udpsender = threading.Thread(target = b)		

udpreceiver.start()
udpsender.start()
