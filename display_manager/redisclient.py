#!/usr/bin/python

import redis

HOST = 'localhost'
PORT = 6379

def redisclient():
	return redis.StrictRedis(host=HOST, port=PORT, db=0, decode_responses=True)

if __name__ == '__main__':
	config = {'lat': 123, 'long': 445, 'key': 'asdf3fdd'}

	r = redisclient()
	r.set('config', config)
	config_out = r.get('config')

	print(config_out)