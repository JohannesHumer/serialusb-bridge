#!/usr/bin/python3
# encoding=utf-8

import time
import configparser
import socket
import serial
import os
import threading
import logging
import signal
import sys
	
time.sleep(22) # warten bis raspberry fertig gestartet hat

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
pluginconfig = configparser.ConfigParser()
pluginconfig.read(lbpconfig + "/serialusb-bridge/serialusb-bridge-config.cfg")

enabled = pluginconfig.get('serialusbbridge-config', 'ENABLED')
miniservername = pluginconfig.get('serialusbbridge-config', 'MINISERVER')
virtualUDPPort = int(pluginconfig.get('serialusbbridge-config', 'UDPPORT'))
anschlussport2 = pluginconfig.get('serialusbbridge-config', 'USB2ID')
usbakt2 = pluginconfig.get('serialusbbridge-config', 'ENABLEDUSB2')
anschlussbaud2 = pluginconfig.get('serialusbbridge-config', 'USB2BAUD')
anschlussport = int(pluginconfig.get('serialusbbridge-config', 'USB2PORT'))
usb2praefix = pluginconfig.get('serialusbbridge-config', 'USB2PRAEFIX')

# ---------------------------------------------
# Durchsuche Loxberry config file für die Miniserverdaten
# ---------------------------------------------
loxberryconfig = configparser.ConfigParser()
loxberryconfig.read(lbsconfig + "/general.cfg")
miniserverIP = loxberryconfig.get(miniservername, 'IPADDRESS')
loxberryIP = loxberryconfig.get('NETWORK', 'IPADDRESS')

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sockloxberryusb2 = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sockloxberryusb2.bind((loxberryIP, anschlussport)) 


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
logging.warning(" Script von USB-2 neu Gestartet    " + zeit)

# ---------------------------------------------
# Exit wenn PlugIn nicht eingeschalten ist
# ---------------------------------------------
if enabled != "1":
	logging.info("SCRIPT USB2 BEENDET DA ES NICHT AKTIVIERT IST")
	sys.exit(-1)
if usbakt2 != "1":
	logging.info("SCRIPT USB2 BEENDET DA ADAPERT NICHT AKTIVIERT IST")
	sys.exit(-1)
	
# ---------------------------------------------
# Serielle Kommunikation
# ---------------------------------------------

s2 = serial.Serial(anschlussport2, anschlussbaud2)					 	#arduino nano Seriallellen Port öffnen

#prüfen ob port offen ist  ; 3 sec warten und nochmal prüfen 3x
i = 0
if s2.isOpen() == False and i <= 3:										
	ser.open()
	i += 1	
	time.sleep(3)
if s2.isOpen() == False and i == 4:					# wenn der port nicht geöffnet werden konnte logdatei schreiben
	logging.error("Script USB-2 Konnte USB Gerät nicht öffnen  :   " + zeit + "\n" + "ID: " + anschlussport2 + "    BAUD: " + anschlussbaud2 + "\n" + "\n")

def a():
		try:   											#überwachung ob fehler sind											#daten von Arduino Nano
			while True :
				data, addr = sockloxberryusb2.recvfrom(1024) 							# buffer ist 1024 bytes und wird von loxone empfangen
				data2 = data
				usberkennung = data2[0:6].decode()  #erkennen ob usb 1,....
				usbdaten = data2[6:]		#usb-x= löschen
				if usberkennung == "USB-2=":	# wenn usb-2 vorgestellt ist die restlichen daten seriell schreiben
					s2.write(usbdaten) # daten seriell schreiben	
					logging.info("DATENWEG USB2 OK UDP ->USB daten  :" + str(usbdaten))
		except Exception as e:
			logging.exception("\n\n\n" + "Fehler bei Script USB-2 Von UDP zu Seriell     " + zeit)				#logeintrag schreiben
			for line in os.popen("ps ax | grep  serialusb-bridge-script-usb2.py | grep -v grep"):			# ganzes script mit threads killen
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)

def b():	
		try:   											#überwachung ob fehler sind
			while True :
					response = s2.readline() 				#Serielles lesen am usb (nano)
					response2 = usb2praefix + response.decode('ISO-8859-1')			# kopie wird erstellt und mit der präfix befüllt
					sock.sendto(response2.encode(),(miniserverIP,virtualUDPPort)) 		#daten werden zu loxone gesendet 
					logging.info("DATENWEG USB2 OK USB -> UDP daten  :" + str(response2))					
		except Exception as e:
			logging.exception("\n\n\n" + "Fehler bei Script USB-2 Von Seriell zu UDP  " + zeit)					#logeintrag schreiben
			for line in os.popen("ps ax | grep  serialusb-bridge-script-usb2.py | grep -v grep"):			# ganzes script mit threads killen
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)
			
#threading das gesendet und empfangen gleichzeit werden kann
udpreceiver = threading.Thread(target = a)		
udpsender = threading.Thread(target = b)		

udpreceiver.start()
udpsender.start()