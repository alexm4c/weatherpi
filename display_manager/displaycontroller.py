#!/usr/bin/python

from lcd import LCD

class DisplayController():
	def __init__(self):
		lcd = LCD()

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

	def update(self):
		display_string = views.time_view()
		display_string = ''
		if not weather:
			display_string = [views.no_data_view()]
		else:
			display_string = [
				views.max_temp(weather),
				views.min_temp(weather),
				views.precip_type(weather),
				views.precip_intensity(weather),
				views.precip_probability(weather),
				views.wind_bearing(weather),
				views.wind_speed(weather),
				views.summary(weather)]

		self.lcd.message(' '.join(display_string))

	# Darksky attributes are not present if they are null. So in each instance we 
	# need to check if the attribute exists and if it doesn't, display some empty 
	# string so it's obvious to the user.
	_EMPTY_ATTRIBUTE = '-'

	def _max_temp(self, forecast):
		string = _EMPTY_ATTRIBUTE

		try:
			temperature_16hr = [hour.temperature for hour in forecast.hourly][:16]
			string = '{max:2.0f}ßC'.format(max=max(temperature_16hr))
		except AttributeError:
			pass
		finally:
			return string

	def _min_temp(self, forecast):
		string = _EMPTY_ATTRIBUTE

		try:
			temperature_16hr = [hour.temperature for hour in forecast.hourly][:16]
			string = '{min:2.0f}ßC'.format(min=min(temperature_16hr))
		except AttributeError:
			pass
		finally:
			return string

	def _current_temp(self, forecast):
		string = _EMPTY_ATTRIBUTE

		try:
			string = '{current:2.0f}ßC'.format(current=forecast.currently.temperature)
		except AttributeError:
			pass
		finally:
			return string

	def _precip_type(self, forecast):
		string = _EMPTY_ATTRIBUTE

		try:
			string = '{type:.4}'.format(type=forecast.currently.precipType.capitalize())
		except AttributeError:
			pass
		finally:
			return string

	def _precip_intensity(self, forecast):
		string = _EMPTY_ATTRIBUTE

		try:
			string = '{intensity:04.2f}mm'.format(intensity=forecast.currently.precipIntensity)
		except AttributeError:
			pass
		finally:
			return string

	def _precip_probability(self, forecast):
		string = _EMPTY_ATTRIBUTE

		try:
			string = '{probability:3.0%}'.format(probability=forecast.currently.precipProbability)
		except AttributeError:
			pass
		finally:
			return string

	def _wind_bearing(self, forecast):
		string = _EMPTY_ATTRIBUTE

		try:
			if not forecast.currently.windBearing:
				# API Docs says if windBearing is 0 it isn't returned
				string = "N"

			elif forecast.currently.windBearing > 337.5 or forecast.currently.windBearing <= 22.5:
				string = "N"

			elif forecast.currently.windBearing <= 67.5:
				string = "NE"

			elif forecast.currently.windBearing <= 112.5:
				string = "E"

			elif forecast.currently.windBearing <= 157.5:
				string = "SE"

			elif forecast.currently.windBearing <= 202.5:
				string = "S"

			elif forecast.currently.windBearing <= 247.5:
				string = "SW"

			elif forecast.currently.windBearing <= 292.5:
				string = "W"
			else:
				string = "NW"
		except AttributeError:
			pass

		return string

	def _wind_speed(self, forecast):
		string = _EMPTY_ATTRIBUTE

		try:
			string = '{speed:4.2f}m/s'.format(speed=forecast.currently.windSpeed)
		except AttributeError:
			pass

		return string

	def _summary(self, forecast):
		string = _EMPTY_ATTRIBUTE

		try:
			string = '{}'.format(forecast.currently.summary)
		except AttributeError:
			pass

		return string

	def _no_data_view(self, ):
		return '{:^20}'.format('No forecast data')
