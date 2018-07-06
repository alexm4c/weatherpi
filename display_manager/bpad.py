#!/usr/bin/python

import RPi.GPIO as GPIO


class Button_Pad(object):
	BUTTON_1 = 5
	BUTTON_2 = 6
	BUTTON_3 = 12
	BUTTON_4 = 13

	def __init__(self):
		GPIO.setmode(GPIO.BCM)

	def _do_func(self, channel, func, *args, **kwargs):
		print('Detected button press on channel {}'.format(channel))
		func(*args, **kwargs)

	def reassign(self, channel, func, *args, **kwargs):
		GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
		GPIO.add_event_detect(
			channel,
			GPIO.FALLING,
			callback=lambda *x: self._do_func(channel, func, *args, **kwargs),
			bouncetime=300)

	def __del__(self):
		GPIO.cleanup()

if __name__ == '__main__':
	import time

	def test(message):
		print('{}'.format(message))

	bp = Button_Pad()
	bp.reassign(bp.BUTTON_1, test, 'test1')
	bp.reassign(bp.BUTTON_2, test, 'test2')

	time.sleep(1e6)