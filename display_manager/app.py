#!/usr/bin/python

import time

import darksky

from rtimer import RepeatedTimer
from backlight import Backlight
from displaycontroller import DisplayController
from bpad import ButtonPad
import views

API_KEY = '3263712d1c1452735faa19a7f9b90edc'
MELBOURNE = (-37.758778, 144.991722)
OPTIONS = {'units': 'si', 'excludes': 'minutely,daily,alerts,flags'}
REFRESH_TIME = 300

class App():
	def __init__(self):
		backlight = Backlight()
		display_controller = DisplayController()
		display_controller.welcome()
		bpad = Button_Pad()
		bpad.reassign(bpad.BUTTON_1, backlight.toggle)
		bpad.reassign(bpad.BUTTON_2, lcd.scroll)
		weather = darksky.forecast(API_KEY, *MELBOURNE, **OPTIONS)

	def run(self):
		try:
			rtimer = RepeatedTimer(REFRESH_TIME, weather.refresh, **OPTIONS)
			while(True):
				display_controller.update()
				time.sleep(1)
		except KeyboardInterrupt:
			print("\nexiting...")
		finally:
			rtimer.stop()
