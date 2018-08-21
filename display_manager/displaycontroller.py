#!/usr/bin/python

import datetime

from lcd import LCD

# Darksky attributes are not present if they are null. So in each instance we 
# need to check if the attribute exists and if it doesn't, display some empty 
# string so it's obvious to the user.

_EMPTY_ATTRIBUTE = '-'

def _max_temp(data):
	temperature_16hr = [hour.temperature for hour in data.hourly][:16]
	return '{max:2.0f}ßC'.format(max=max(temperature_16hr))


def _min_temp(data):
	temperature_16hr = [hour.temperature for hour in data.hourly][:16]
	return '{min:2.0f}ßC'.format(min=min(temperature_16hr))

def _precip_type(data):
	precip_type = getattr(data.currently, 'precipType', None)
	if precip_type:
		string = '{type:.4}'.format(type=precip_type.capitalize())
	else:
		string = _EMPTY_ATTRIBUTE
	return string

def _precip_intensity(data):
	precip_intensity = getattr(data.currently, 'precipIntensity', None)
	if precip_intensity:
		string = '{intensity:04.2f}mm'.format(intensity=precip_intensity)
	else:
		string = _EMPTY_ATTRIBUTE
	return string

def _precip_probability(data):
	precip_probability = getattr(data.currently, 'precipProbability', None)
	if precip_probability:
		string = '{probability:3.0%}'.format(probability=precip_probability)
	else:
		string = _EMPTY_ATTRIBUTE
	return string

def _wind_bearing(data):
	wind_bearing = getattr(data.currently, 'windBearing', None)

	if not wind_bearing:
		# API Docs says if windBearing is 0 it isn't returned
		string = "N"

	elif wind_bearing > 337.5 or wind_bearing <= 22.5:
		string = "N"

	elif wind_bearing <= 67.5:
		string = "NE"

	elif wind_bearing <= 112.5:
		string = "E"

	elif wind_bearing <= 157.5:
		string = "SE"

	elif wind_bearing <= 202.5:
		string = "S"

	elif wind_bearing <= 247.5:
		string = "SW"

	elif wind_bearing <= 292.5:
		string = "W"
	else:
		string = "NW"

	return string

def _wind_speed(data):
	wind_speed = getattr(data.currently, 'windSpeed', None)
	if wind_speed:
		string = '{speed:4.2f}m/s'.format(speed=wind_speed)
	else:
		string = _EMPTY_ATTRIBUTE
	return string

def _summary(data):
	return  '{}'.format(data.currently.summary)

def _no_data():
	return '{:^20}'.format('No forecast data')

def _date_time():
	return '{:%d %b %H%M}'.format(datetime.datetime.now())

class DisplayController():
	def __init__(self):
		self.lcd = LCD()

	def welcome(self):
		welcome_animation = [
		'ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ',
		'ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ  ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ',
		'ÿÿÿÿÿÿÿÿ  ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ th ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ     ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ   ÿÿÿÿÿÿÿÿÿ',
		'ÿÿÿÿÿÿÿ     ÿÿÿÿÿÿÿÿÿÿÿÿÿÿ ather ÿÿÿÿÿÿÿÿÿÿÿÿÿ       ÿÿÿÿÿÿÿÿÿÿÿÿÿÿ     ÿÿÿÿÿÿÿÿ',
		'ÿÿÿÿÿÿ       ÿÿÿÿÿÿÿÿÿÿÿÿ eatherP ÿÿÿÿÿÿÿÿÿÿÿ         ÿÿÿÿÿÿÿÿÿÿÿÿ       ÿÿÿÿÿÿÿ',
		'ÿÿÿÿÿ         ÿÿÿÿÿÿÿÿÿÿ WeatherPi ÿÿÿÿÿÿÿÿÿ           ÿÿÿÿÿÿÿÿÿÿ         ÿÿÿÿÿÿ',
		'ÿÿÿÿ           ÿÿÿÿÿÿÿÿ  WeatherPi  ÿÿÿÿÿÿÿ             ÿÿÿÿÿÿÿÿ           ÿÿÿÿÿ',
		'ÿÿÿ             ÿÿÿÿÿÿ   WeatherPi   ÿÿÿÿÿ               ÿÿÿÿÿÿ             ÿÿÿÿ',
		'ÿÿ               ÿÿÿÿ    WeatherPi    ÿÿÿ                 ÿÿÿÿ               ÿÿÿ',
		'ÿ                 ÿÿ     WeatherPi     ÿ                   ÿÿ                 ÿÿ',
		'                         WeatherPi                                              ']
		for frame in welcome_animation:
			self.lcd.message(frame)

	def update(self, data):
		if not data:
			display_string = [_no_data()]
		else:
			display_string = [
				_date_time(),
				_max_temp(data),
				_min_temp(data),
				_precip_type(data),
				_precip_intensity(data),
				_precip_probability(data),
				_wind_bearing(data),
				_wind_speed(data),
				_summary(data)]

		self.lcd.message(' '.join(display_string))

	def scroll(self):
		self.lcd.scroll()