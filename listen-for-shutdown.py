#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import subprocess

# we will use the pin numbering to match the pins on the Pi, instead of the 
# GPIO pin outs (makes it easier to keep track of things)

GPIO.setmode(GPIO.BCM)  

POWER_BTN_PIN = 3  #power button GPIO Pin 
RESET_BTN_PIN =	2 #reset button GPIO Pin 

# use the same pin that is used for the reset button (one button to rule them all!)
GPIO.setup(POWER_BTN_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)  	#INPUT:  Setup POWER button
GPIO.setup(RESET_BTN_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)  	#INPUT:  Setup RESET button

bounce_time = 2000

#PYTHON Functions
def Shutdown(channel):
	for i in range(0,20):
		time.sleep(0.1)
		#GPIO.input(POWER_BTN_PIN)
		os.system("sudo shutdown -h now")

def Reset(channel):
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
	try:
		commandpath = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
		if commandpath[0:24] == '/opt/retropie/emulators/':
			os.system('kill -TERM %s' % pid)
			print('kill -TERM %s ...' % pid)
			i = 0
			while i < 10:
				i = i + 1
				# probably we should again check here.. but.. nah
				os.system('kill -KILL %s' % pid)
				print('kill -KILL %s' % pid)
	except IOError:
		continue
    
GPIO.add_event_detect(POWER_BTN_PIN, GPIO.RISING, callback=Shutdown, bouncetime = bounce_time) 
GPIO.add_event_detect(RESET_BTN_PIN, GPIO.RISING, callback=Reset,bouncetime = bounce_time)
