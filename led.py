#!/usr/bin/python

import RPi.GPIO as GPIO

class LED(object):
	
	
	def __init__(self):
		self._PIN = 16
		self.is_on = True
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self._PIN, GPIO.OUT)
		GPIO.output(self._PIN, GPIO.HIGH)

	def __del__(self):
		GPIO.cleanup()

	def toggle(self):
		if self.is_on:
			GPIO.output(self._PIN, GPIO.HIGH)
		else:
			GPIO.output(self._PIN, GPIO.LOW)
		self.is_on = not self.is_on
