#!/usr/bin/python

from app import App

app = App()
try:
	app.run()
except KeyboardInterrupt:
	print('exiting...')