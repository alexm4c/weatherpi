#!/usr/bin/python

from lcd import LCD

# Darksky attributes are not present if they are null. So in each instance we 
# need to check if the attribute exists and if it doesn't, display some empty 
# string so it's obvious to the user.
_EMPTY_ATTRIBUTE = '-'

def _max_temp(data):
	string = _EMPTY_ATTRIBUTE

	try:
		temperature_16hr = [hour.temperature for hour in data.hourly][:16]
		string = '{max:2.0f}ßC'.format(max=max(temperature_16hr))
	except AttributeError:
		pass
	finally:
		return string

def _min_temp(data):
	string = _EMPTY_ATTRIBUTE

	try:
		temperature_16hr = [hour.temperature for hour in data.hourly][:16]
		string = '{min:2.0f}ßC'.format(min=min(temperature_16hr))
	except AttributeError:
		pass
	finally:
		return string

def _current_temp(data):
	string = _EMPTY_ATTRIBUTE

	try:
		string = '{current:2.0f}ßC'.format(current=data.currently.temperature)
	except AttributeError:
		pass
	finally:
		return string

def _precip_type(data):
	string = _EMPTY_ATTRIBUTE

	try:
		string = '{type:.4}'.format(type=data.currently.precipType.capitalize())
	except AttributeError:
		pass
	finally:
		return string

def _precip_intensity(data):
	string = _EMPTY_ATTRIBUTE

	try:
		string = '{intensity:04.2f}mm'.format(intensity=data.currently.precipIntensity)
	except AttributeError:
		pass
	finally:
		return string

def _precip_probability(data):
	string = _EMPTY_ATTRIBUTE

	try:
		string = '{probability:3.0%}'.format(probability=data.currently.precipProbability)
	except AttributeError:
		pass
	finally:
		return string

def _wind_bearing(data):
	string = _EMPTY_ATTRIBUTE

	try:
		if not data.currently.windBearing:
			# API Docs says if windBearing is 0 it isn't returned
			string = "N"

		elif data.currently.windBearing > 337.5 or data.currently.windBearing <= 22.5:
			string = "N"

		elif data.currently.windBearing <= 67.5:
			string = "NE"

		elif data.currently.windBearing <= 112.5:
			string = "E"

		elif data.currently.windBearing <= 157.5:
			string = "SE"

		elif data.currently.windBearing <= 202.5:
			string = "S"

		elif data.currently.windBearing <= 247.5:
			string = "SW"

		elif data.currently.windBearing <= 292.5:
			string = "W"
		else:
			string = "NW"
	except AttributeError:
		pass

	return string

def _wind_speed(data):
	string = _EMPTY_ATTRIBUTE

	try:
		string = '{speed:4.2f}m/s'.format(speed=data.currently.windSpeed)
	except AttributeError:
		pass

	return string

def _summary(data):
	string = _EMPTY_ATTRIBUTE

	try:
		string = '{}'.format(data.currently.summary)
	except AttributeError:
		pass

	return string

def _no_data_view():
	return '{:^20}'.format('No forecast data')



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
		# display_string = _time_view()
		display_string = ''
		if not data:
			display_string = [_no_data_view()]
		else:
			display_string = [
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