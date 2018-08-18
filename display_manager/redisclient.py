#!/usr/bin/python

import redis

HOST = 'localhost'
PORT = 6379

def redis_client():
	return redis.StrictRedis(host=HOST, port=PORT, db=0, decode_responses=True)