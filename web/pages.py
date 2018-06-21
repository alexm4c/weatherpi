#!/usr/bin/python

# this is suitable for a GET - it has no parameters
def home():
	response = '<!DOCTYPE html>\n<html>\n'
	response += '<head><title>WeatherPi</title></head>\n'
	response += '<body>WeatherPi Config</body>\n'
	response += '</html>'

	return response

def submit(form):
	response = '<!DOCTYPE html>\n<html>\n'
	response += '<head><title>WeatherPi</title></head>\n'
	response += '<body>WeatherPi Config</body>\n'
	response += '</html>'

	return response