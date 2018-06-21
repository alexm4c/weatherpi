from datetime import datetime

def time_view():
	return '{:%d %b         %H:%M}'.format(datetime.now())

def temperature_view(forecast):
	temperature_12hr = [hour.temperature for hour in forecast.hourly][:12]
	return '{max:2.0f}ßC {current:2.0f}ßC {min:2.0f}ßC      '.format(
		current = forecast.currently.temperature,
		max = max(temperature_12hr),
		min = min(temperature_12hr))

def precipitation_view(forecast):
	return '{type:.4} {intensity:04.2f}mm {probability:3.0%}     '.format(
		type = forecast.currently.precipType.capitalize(),
		intensity = forecast.currently.precipIntensity,
		probability = forecast.currently.precipProbability)

def wind_view(forecast):
	bearing = ''
	if forecast.currently.windBearing == None:
		#API Docs says if windBearing is 0 it isn't returned
		bearing = "N"

	elif forecast.currently.windBearing > 337.5 or forecast.currently.windBearing <= 22.5:
		bearing = "N"

	elif forecast.currently.windBearing <= 67.5:
		bearing = "NE"

	elif forecast.currently.windBearing <= 112.5:
		bearing = "E"

	elif forecast.currently.windBearing <= 157.5:
		bearing = "SE"

	elif forecast.currently.windBearing <= 202.5:
		bearing = "S"

	elif forecast.currently.windBearing <= 247.5:
		bearing = "SW"

	elif forecast.currently.windBearing <= 292.5:
		bearing = "W"
	else:
		bearing = "NW"

	return '{speed:4.2f}m/s{bearing:>13}'.format(
		speed = forecast.currently.windSpeed,
		bearing = bearing)

def no_data_view():
	return '{:^20}'.format('No forecast data')

def summary_view(forecast):
	return '{}'.format(forecast.currently.summary)


