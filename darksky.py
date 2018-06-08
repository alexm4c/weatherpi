#!/usr/bin/python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
# from StringIO import StringIO
import gzip
import urllib.request
import urllib.error
import json

API_HOST = "https://api.darksky.net/forecast"
API_KEY = "3263712d1c1452735faa19a7f9b90edc"
API_OPTIONS = "units=si&exclude=minutely,daily,alerts,flags"

latitude = -37.758778
longitude = 144.991722

class Forecast:

	def __init__(self):
		self.key = API_KEY
		self.options = API_OPTIONS
		self.latitude = latitude
		self.longitude = longitude
		self.shed = BackgroundScheduler()
		self.shed.add_job(self.update, 'interval', minutes=5, next_run_time=datetime.now())
		self.shed.start()
		self.data = None

	def __del__(self):
		self.shed.shutdown()

	def get_forecast_data(self):
		return self.data

	def update(self):
		uri_format = '{host}/{key}/{latitude},{longitude}?{options}'
		url = uri_format.format(
			host=API_HOST,
			key=self.key, 
			latitude=self.latitude,
			longitude=self.longitude,
			options=self.options)

		request = urllib.request.Request(
			url,
			headers={'Accept-Encoding': 'gzip'})		
		
		response = urllib.request.urlopen(request)
		result = gzip.decompress(response.read())
		result = result.decode('utf-8')
		self.data = json.loads(result)

if __name__ == '__main__':
	forecast = Forecast()
	forecast.update()
	print(forecast.get_forecast_data())