#!/usr/bin/python

import time
import RPi.GPIO as GPIO

button = 17
led_switch = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_switch, GPIO.OUT)

is_on = True
GPIO.output(led_switch, GPIO.HIGH)

def on_button_trigger(channel):
	global is_on
	if is_on:
		GPIO.output(led_switch, GPIO.HIGH)
	else:
		GPIO.output(led_switch, GPIO.LOW)
	is_on = not is_on

GPIO.add_event_detect(button, GPIO.FALLING, callback=on_button_trigger, bouncetime=300)

try:
	while(True):
		time.sleep(1e6)
except KeyboardInterrupt:
	GPIO.cleanup()
	print("\nexiting...")
