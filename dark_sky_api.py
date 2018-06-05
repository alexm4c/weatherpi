#!/usr/bin/python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from StringIO import StringIO
import gzip
import urllib2
import json

API_HOST = "https://api.forecast.io/forecast/"
API_KEY = "3263712d1c1452735faa19a7f9b90edc"
API_OPTIONS = "?units=si&exclude=minutely,daily,alerts,flags"

latitude = -37.758778
longitude = 144.991722

class Dark_Sky_API:

	def __init__(self):
		self.host = API_HOST
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
		url = self.host
		url += self.key
		url += "/"
		url += str(self.latitude) 
		url += "," 
		url += str(self.longitude)
		if self.options:
			url += self.options
		
		req = urllib2.Request(url)
		req.add_header('Accept-Encoding', 'gzip')
		res = urllib2.urlopen(req)
		data = res.read()

		if res.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(data)
			data = gzip.GzipFile(fileobj=buf).read()

		self.data = json.loads(data)

