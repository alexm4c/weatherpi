#!/usr/bin/python

import time
from datetime import datetime
from darksky import forecast
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO

API_KEY = '3263712d1c1452735faa19a7f9b90edc'
MELBOURNE = (-37.758778, 144.991722)
OPTIONS = {'units': 'si', 'excludes': 'minutely,daily,alerts,flags'}

# LCD pin configuration
lcd_rs = 27
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18

# LCD dimensions
lcd_columns = 20
lcd_rows    = 4

# Initialise LCD
lcd = LCD.Adafruit_CharLCD(
	lcd_rs,
	lcd_en,
	lcd_d4,
	lcd_d5,
	lcd_d6,
	lcd_d7,
	lcd_columns,
	lcd_rows)

display_string = ""
scroll_depth = 0
scroll_button = 4
led_button = 17
led_switch = 5
led_is_on = True

def format_for_LCD(message):
	# Slice a message exactly as long as the LCD has characters beginning at the scroll_depth-th row
	string = message[scroll_depth*lcd_columns:scroll_depth*lcd_columns+(lcd_columns*lcd_rows)]
	string = string.ljust(lcd_columns*lcd_rows)
	string = '\n'.join([string[i:i+lcd_columns] for i in range(0, len(string), lcd_columns)])
	return string

def scroll(channel):
	global scroll_depth
	global display_string
	# Calculate maximum scroll depth based on display_string length
	if scroll_depth > (len(display_string) / lcd_columns) - lcd_rows:
		scroll_depth = 0
	else:
		scroll_depth += 1

def led_on_off(channel):
	global led_is_on
	if led_is_on:
		GPIO.output(led_switch, GPIO.HIGH)
	else:
		GPIO.output(led_switch, GPIO.LOW)
	led_is_on = not led_is_on

# Setup GPIO 
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_switch, GPIO.OUT)
GPIO.setup(scroll_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(led_switch, GPIO.HIGH)

GPIO.add_event_detect(led_button, GPIO.FALLING, callback=led_on_off, bouncetime=300)
GPIO.add_event_detect(scroll_button, GPIO.FALLING, callback=scroll, bouncetime=300)

# Initialise forcast api
melbourne = forecast(API_KEY, *MELBOURNE, **OPTIONS)

try:
	while(True):
		
		# display_string = time.asctime(time.localtime(time.time()))[:lcd_columns]
		display_string = '{:%d %b         %H:%M}'.format(datetime.now())

		if not melbourne:
			display_string += 'No forecast data'
			continue

		# Format temperature
		temperature_12hr = [hour.temperature for hour in melbourne.hourly][:12]
		temperature_format = ' {current:2.1f}ßC   {max:2.0f}ßC/{min:2.0f}ßC '

		display_string += temperature_format.format(
			current = melbourne.currently.temperature,
			max = max(temperature_12hr),
			min = min(temperature_12hr))
		
		# Format precipitation
		precipitation_format = ' {type:.4} {probability:3.0f}%  {intensity:04.2f}mm  '
		
		display_string += precipitation_format.format(
			type = melbourne.currently.precipType.capitalize(),
			intensity = melbourne.currently.precipIntensity,
			probability = melbourne.currently.precipProbability)

		# Format wind
		bearing = ''
		if melbourne.currently.windBearing == None:
			#API Docs says if windBearing is 0 it isn't returned
			bearing = "N"

		elif melbourne.currently.windBearing > 337.5 or melbourne.currently.windBearing <= 22.5:
			bearing = "N"

		elif melbourne.currently.windBearing <= 67.5:
			bearing = "NE"

		elif melbourne.currently.windBearing <= 112.5:
			bearing = "E"

		elif melbourne.currently.windBearing <= 157.5:
			bearing = "SE"

		elif melbourne.currently.windBearing <= 202.5:
			bearing = "S"

		elif melbourne.currently.windBearing <= 247.5:
			bearing = "SW"

		elif melbourne.currently.windBearing <= 292.5:
			bearing = "W"

		else:
			bearing = "NW"

		wind_format = ' {speed:4.2f}m/s {bearing:1}          '
		
		display_string += wind_format.format(
			speed = melbourne.currently.windSpeed,
			bearing = bearing)

		# Format summary
		display_string += melbourne.currently.summary

		lcd.message(format_for_LCD(display_string))
		
		time.sleep(1)

except KeyboardInterrupt:
	print("\nexiting...")
	GPIO.cleanup()
