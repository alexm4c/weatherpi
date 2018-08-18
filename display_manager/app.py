#!/usr/bin/python

import time

import darksky

from rtimer import RepeatedTimer
from backlight import Backlight
from displaycontroller import DisplayController
from bpad import ButtonPad
from config import Config

OPTIONS = {'units': 'si'}

class App():
	def __init__(self):
		self.backlight = Backlight()
		self.display_controller = DisplayController()
		self.display_controller.welcome()
		self.bpad = ButtonPad()
		self.bpad.reassign(self.bpad.BUTTON_1, self.backlight.toggle)
		self.bpad.reassign(self.bpad.BUTTON_2, self.display_controller.scroll)
		self.config = Config()
		self.darksky = darksky.forecast(self.config.api_key, self.config.latitude, self.config.longitude, **OPTIONS)

	def run(self):
		rtimer = RepeatedTimer(self.config.refresh_time, self.darksky.refresh, **OPTIONS)
		try:
			while(True):
				self.display_controller.update(self.darksky)
				time.sleep(1)
		except KeyboardInterrupt:
			print("\nexiting...")
		finally:
			rtimer.stop()
