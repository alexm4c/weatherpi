#!/usr/bin/python

import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO

# Pin configuration:
lcd_rs        = 27
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18

lcd_columns = 20
lcd_rows    = 4

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

output = ""
scroll_level = 0

button = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def scroll(channel):
	global output
	global scroll_level
	max_scroll_level = (len(output) % lcd_columns) / lcd_rows
	if scroll_level > max_scroll_level:
		scroll_level = 0
	else:
		scroll_level += 1

GPIO.add_event_detect(button, GPIO.FALLING, callback=scroll, bouncetime=300)

try:
	while(True):
		time_str = time.asctime(time.localtime(time.time()))[:lcd_columns]
		output = time_str + "hello my name is alex and this is my test message blah blah who cares this is a test line testing please ignore lol"
		msg = output[scroll_level*lcd_columns:min((scroll_level*lcd_columns)+(lcd_columns*lcd_rows), len(output))]
		msg = msg.ljust(lcd_columns*lcd_rows)
		msg = '\n'.join([msg[i:i+lcd_columns] for i in range(0, len(msg), lcd_columns)])

		lcd.message(msg)
		time.sleep(0.1)
except KeyboardInterrupt:
	print("\nexiting...")
