#!/usr/bin/python

import time

from darksky import forecast

from rtimer import RepeatedTimer
from lcd import LCD
import views

API_KEY = '3263712d1c1452735faa19a7f9b90edc'
MELBOURNE = (-37.758778, 144.991722)
OPTIONS = {'units': 'si', 'excludes': 'minutely,daily,alerts,flags'}
REFRESH_TIME = 300

try:	
	lcd = LCD()
	
	# Initialise forcast api
	weather = forecast(API_KEY, *MELBOURNE, **OPTIONS)
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