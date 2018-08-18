#!/usr/bin/python

from redisclient import redis_client

class Config(object):
	def __init__(self):
		_schema = {
			'api_key': str,
			'latitude': float,
			'longitude': float,
			'refresh_time': int
		}	
		
		self._read()


	def _read(self):
		redis = redis_client()
		config = {}
		for key, func in self.schema.items():
			try:
				config[key] = func(redis.get(key))
			except ValueError:
				raise
		self.__dict__ = config