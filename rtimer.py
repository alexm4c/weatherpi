#!/usr/bin/python

from threading import Timer

class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self.timer = None
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False


if __name__ == '__main__':
	from time import sleep

	def test(x):
		print('testing {}'.format(x))

	rt = RepeatedTimer(1, test, "!!!")

	try:
		sleep(5)
	finally:
		rt.stop()