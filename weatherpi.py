#!/usr/bin/python

import time

import darksky

from rtimer import RepeatedTimer
from lcd import LCD
from bpad import Button_Pad
from led import LED
import views

API_KEY = '3263712d1c1452735faa19a7f9b90edc'
MELBOURNE = (-37.758778, 144.991722)
OPTIONS = {'units': 'si', 'excludes': 'minutely,daily,alerts,flags'}
REFRESH_TIME = 300

try:
	# Init lcd led
	led = LED()

	# Init lcd
	lcd = LCD()
	welcome_animation = (
	'ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ',
	'ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ',
	'ÿÿÿÿÿÿÿÿ  ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ th ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ    ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ  ÿÿÿÿÿÿÿÿÿÿ',
	'ÿÿÿÿÿÿÿ     ÿÿÿÿÿÿÿÿÿÿÿÿÿÿ ather ÿÿÿÿÿÿÿÿÿÿÿÿÿ       ÿÿÿÿÿÿÿÿÿÿÿÿÿÿ     ÿÿÿÿÿÿÿÿ',
	'ÿÿÿÿÿÿ       ÿÿÿÿÿÿÿÿÿÿÿÿ eatherP ÿÿÿÿÿÿÿÿÿÿÿ         ÿÿÿÿÿÿÿÿÿÿÿÿ       ÿÿÿÿÿÿÿ',
	'ÿÿÿÿÿ         ÿÿÿÿÿÿÿÿÿÿ WeatherPi ÿÿÿÿÿÿÿÿÿ           ÿÿÿÿÿÿÿÿÿÿ         ÿÿÿÿÿÿ',
	'ÿÿÿÿ           ÿÿÿÿÿÿÿÿ  WeatherPi  ÿÿÿÿÿÿÿ             ÿÿÿÿÿÿÿÿ           ÿÿÿÿÿ',
	'ÿÿÿ             ÿÿÿÿÿÿ   WeatherPi   ÿÿÿÿÿ               ÿÿÿÿÿÿ             ÿÿÿÿ',
	'ÿÿ               ÿÿÿÿ    WeatherPi    ÿÿÿ                 ÿÿÿÿ               ÿÿÿ',
	'ÿ                 ÿÿ     WeatherPi     ÿ                   ÿÿ                 ÿÿ',
	'                         WeatherPi                                              ')

	for frame in welcome_animation:
		lcd.message(frame)

	# Init buttons
	bpad = Button_Pad()
	bpad.reassign(bpad.BUTTON_1, led.toggle)
	# bpad.reassign(BUTTON_2, )

	# Init forcast api
	weather = darksky.forecast(API_KEY, *MELBOURNE, **OPTIONS)
	rtimer = RepeatedTimer(REFRESH_TIME, weather.refresh, **OPTIONS)

	while(True):
		# display_string = views.time_view()
		display_string = ''
		if not weather:
			display_string += views.no_data_view()
		else:
			display_string += views.max_temp(weather)
			display_string += ' '
			display_string += views.min_temp(weather)
			display_string += ' '
			display_string += views.precip_type(weather)
			display_string += ' '
			display_string += views.precip_intensity(weather)
			display_string += ' '
			display_string += views.precip_probability(weather)
			display_string += ' '
			display_string += views.wind_bearing(weather)
			display_string += ' '
			display_string += views.wind_speed(weather)
			display_string += ' '
			display_string += views.summary(weather)

		lcd.message(display_string)
		time.sleep(1)

except KeyboardInterrupt:
	print("\nexiting...")

finally:
	rtimer.stop()