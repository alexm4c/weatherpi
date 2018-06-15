#!/usr/bin/python

import time
from datetime import datetime

from darksky import forecast
from repeated_timer import RepeatedTimer
from lcd import LCD

API_KEY = '3263712d1c1452735faa19a7f9b90edc'
MELBOURNE = (-37.758778, 144.991722)
OPTIONS = {'units': 'si', 'excludes': 'minutely,daily,alerts,flags'}
REFRESH_TIME = 300

# Initialise forcast api
melbourne = forecast(API_KEY, *MELBOURNE, **OPTIONS)

lcd = LCD()

try:
	rt = RepeatedTimer(REFRESH_TIME, melbourne.refresh, **OPTIONS)
	
	while(True):
		
		# display_string = time.asctime(time.localtime(time.time()))[:lcd_columns]
		display_string = '{:%d %b         %H:%M}'.format(datetime.now())

		if not melbourne:
			display_string += 'No forecast data'
			continue

		# Format temperature
		temperature_12hr = [hour.temperature for hour in melbourne.hourly][:12]
		temperature_format = '{max:2.0f}ßC {current:2.0f}ßC {min:2.0f}ßC      '

		display_string += temperature_format.format(
			current = melbourne.currently.temperature,
			max = max(temperature_12hr),
			min = min(temperature_12hr))
		
		# Format precipitation
		precipitation_format = '{type:.4} {intensity:04.2f}mm {probability:3.0%}     '
		
		display_string += precipitation_format.format(
			type = melbourne.currently.precipType.capitalize(),
			intensity = melbourne.currently.precipIntensity,
			probability = melbourne.currently.precipProbability)

		# # Format wind
		# bearing = ''
		# if melbourne.currently.windBearing == None:
		# 	#API Docs says if windBearing is 0 it isn't returned
		# 	bearing = "N"

		# elif melbourne.currently.windBearing > 337.5 or melbourne.currently.windBearing <= 22.5:
		# 	bearing = "N"

		# elif melbourne.currently.windBearing <= 67.5:
		# 	bearing = "NE"

		# elif melbourne.currently.windBearing <= 112.5:
		# 	bearing = "E"

		# elif melbourne.currently.windBearing <= 157.5:
		# 	bearing = "SE"

		# elif melbourne.currently.windBearing <= 202.5:
		# 	bearing = "S"

		# elif melbourne.currently.windBearing <= 247.5:
		# 	bearing = "SW"

		# elif melbourne.currently.windBearing <= 292.5:
		# 	bearing = "W"
		# else:
		# 	bearing = "NW"

		# wind_format = '{speed:4.2f}m/s{bearing:>13}'.ljust(lcd_columns)
		# display_string += wind_format.format(
		# 	speed = melbourne.currently.windSpeed,
		# 	bearing = bearing)

		# Format summary
		display_string += melbourne.currently.summary

		lcd.message(display_string)
		
		time.sleep(1)

except KeyboardInterrupt:
	print("\nexiting...")
finally:
	rt.stop()
