#!/usr/bin/python

# Darksky attributes are not present if they are null. So in each instance we 
# need to check if the attribute exists and if it doesn't, display some empty 
# string so it's obvious to the user.
EMPTY = '-'

def max_temp(forecast):
	string = EMPTY

	try:
		temperature_16hr = [hour.temperature for hour in forecast.hourly][:16]
		string = '{max:2.0f}ßC'.format(max=max(temperature_16hr))
	except AttributeError:
		pass
	finally:
		return string

def min_temp(forecast):
	string = EMPTY

	try:
		temperature_16hr = [hour.temperature for hour in forecast.hourly][:16]
		string = '{min:2.0f}ßC'.format(min=min(temperature_16hr))
	except AttributeError:
		pass
	finally:
		return string

def current_temp(forecast):
	string = EMPTY

	try:
		string = '{current:2.0f}ßC'.format(current=forecast.currently.temperature)
	except AttributeError:
		pass
	finally:
		return string

def precip_type(forecast):
	string = EMPTY

	try:
		string = '{type:.4}'.format(type=forecast.currently.precipType.capitalize())
	except AttributeError:
		pass
	finally:
		return string

def precip_intensity(forecast):
	string = EMPTY

	try:
		string = '{intensity:04.2f}mm'.format(intensity=forecast.currently.precipIntensity)
	except AttributeError:
		pass
	finally:
		return string

def precip_probability(forecast):
	string = EMPTY

	try:
		string = '{probability:3.0%}'.format(probability=forecast.currently.precipProbability)
	except AttributeError:
		pass
	finally:
		return string

def wind_bearing(forecast):
	string = EMPTY

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

def wind_speed(forecast):
	string = EMPTY

	try:
		string = '{speed:4.2f}m/s'.format(speed=forecast.currently.windSpeed)
	except AttributeError:
		pass

	return string

def summary(forecast):
	string = EMPTY

	try:
		string = '{}'.format(forecast.currently.summary)
	except AttributeError:
		pass

	return string

def no_data_view():
	return '{:^20}'.format('No forecast data')
