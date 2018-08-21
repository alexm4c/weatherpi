#!/usr/bin/python

import time
import logging

import darksky

from rtimer import RepeatedTimer
from backlight import Backlight
from displaycontroller import DisplayController
from bpad import ButtonPad
from config import Config

OPTIONS = {'units': 'si'}

class App(object):
	def __init__(self):
		backlight = Backlight()
		self.display_controller = DisplayController()
		self.display_controller.welcome()
		bpad = ButtonPad()
		bpad.reassign(bpad.BUTTON_1, backlight.toggle)
		bpad.reassign(bpad.BUTTON_2, self.display_controller.scroll)
		self.config = Config()
		self.darksky = darksky.forecast(self.config.api_key, self.config.latitude, self.config.longitude, **OPTIONS)

	def run(self):
		with RepeatedTimer(self.config.refresh_time, self.darksky.refresh, **OPTIONS):
			while(True):
				self.display_controller.update(self.darksky)
				time.sleep(1)
