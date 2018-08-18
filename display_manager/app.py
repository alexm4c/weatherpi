#!/usr/bin/python

import time

import darksky

from rtimer import RepeatedTimer
from backlight import Backlight
from displaycontroller import DisplayController
from bpad import ButtonPad
from config import Config

API_KEY = '3263712d1c1452735faa19a7f9b90edc'
MELBOURNE = (-37.758778, 144.991722)
OPTIONS = {'units': 'si'}
REFRESH_TIME = 300

class App():
	def __init__(self):
		backlight = Backlight()
		display_controller = DisplayController()
		display_controller.welcome()
		bpad = Button_Pad()
		bpad.reassign(bpad.BUTTON_1, backlight.toggle)
		bpad.reassign(bpad.BUTTON_2, lcd.scroll)
		config = Config()
		weather = darksky.forecast(config.api_key, config.coordinates, **OPTIONS)

	def run(self):
		try:
			rtimer = RepeatedTimer(config.refresh_time, weather.refresh, **OPTIONS)
			while(True):
				display_controller.update()
				time.sleep(1)
		except KeyboardInterrupt:
			print("\nexiting...")
		finally:
			rtimer.stop()
