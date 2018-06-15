#!/usr/bin/python

from time import sleep

import RPi.GPIO as GPIO

# scroll_button = 4
led_button = 17
led_switch = 5
led_is_on = True

# def scroll(channel):
# 	LCD().scroll

def led_on_off(channel):
	global led_is_on
	if led_is_on:
		GPIO.output(led_switch, GPIO.HIGH)
	else:
		GPIO.output(led_switch, GPIO.LOW)
	led_is_on = not led_is_on

# Setup GPIO 
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_switch, GPIO.OUT)
# GPIO.setup(scroll_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(led_switch, GPIO.HIGH)

GPIO.add_event_detect(led_button, GPIO.FALLING, callback=led_on_off, bouncetime=300)
# GPIO.add_event_detect(scroll_button, GPIO.FALLING, callback=scroll, bouncetime=300)

try:
	sleep(1e6)
finally:
	GPIO.cleanup()