#!/usr/bin/python3
# encoding=utf-8

import os
import logging
import time
import signal
import subprocess



lbplog = os.environ['LBPLOG']

zeit = time.strftime("%d.%m.%Y %H:%M:%S")
logging.basicConfig(filename= lbplog + '/serialusb-bridge/serialusb-bridge.log', filemode='a', level=logging.WARNING) #logging starten und die einträge anfügen


logging.warning("Neustart für USB Seriell Scripte über Homepage begonnen" + zeit)
for line in os.popen("ps ax | grep  serialusb-bridge-script-usb1.py | grep -v grep"):			# ganzes script mit threads killen
			if line.find("usb1"):
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)			
for line in os.popen("ps ax | grep  serialusb-bridge-script-usb2.py | grep -v grep"):			# ganzes script mit threads killen
			if line.find("usb2"):
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)
for line in os.popen("ps ax | grep  serialusb-bridge-script-usb3.py | grep -v grep"):			# ganzes script mit threads killen
			if line.find("usb3"):
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)
for line in os.popen("ps ax | grep  serialusb-bridge-script-usb4.py | grep -v grep"):			# ganzes script mit threads killen
			if line.find("usb4"):
				fields = line.split()
				pid = fields[0]
				os.kill(int(pid), signal.SIGKILL)
p = subprocess.call("python REPLACELBPBINDIR/serialusb-bridge-script-usb1.py &", shell=True, stdout=subprocess.PIPE) # Prozesse im Hintergrund starten &
p = subprocess.call("python REPLACELBPBINDIR/serialusb-bridge-script-usb2.py &", shell=True, stdout=subprocess.PIPE) # Prozesse im Hintergrund starten &
p = subprocess.call("python REPLACELBPBINDIR/serialusb-bridge-script-usb3.py &", shell=True, stdout=subprocess.PIPE) # Prozesse im Hintergrund starten &
p = subprocess.call("python REPLACELBPBINDIR/serialusb-bridge-script-usb4.py &", shell=True, stdout=subprocess.PIPE) # Prozesse im Hintergrund starten &
logging.warning("Neustart der Scripte ERFOLGREICH Abgeschlossen  WAIT ABOUT 1 MINUTE!!" + zeit)