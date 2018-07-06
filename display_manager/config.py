#!/usr/bin/python

from redisclient import redisclient

schema = {
	'api_key': str,
	'latitude': float,
	'longitude': float,
	'refresh_time': int}

def read():
	redis = redisclient()
	config = {}
	for key, func in schema.items():
		try:
			config[key] = func(redis.get(key))
		except ValueError:
			raise
	return config

def write(config):
	redis = redisclient()
	for key, func in schema.items():
		try:
			redis.set(key, func(config[key]))
		except ValueError:
			raise
