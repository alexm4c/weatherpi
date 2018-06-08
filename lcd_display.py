#!/usr/bin/python

import time
from darksky import Forecast
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO

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
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

def format_for_LCD(message):
	# Slice a message exactly as long as the LCD has characters beginning at the scroll_depth-th row
	string = message[scroll_depth*lcd_columns:scroll_depth*lcd_columns+(lcd_columns*lcd_rows)]
	string = string.ljust(lcd_columns*lcd_rows)
	string = '\n'.join([string[i:i+lcd_columns] for i in range(0, len(string), lcd_columns)])
	return string

display_string = ""
scroll_depth = 0

def scroll(channel):
	global scroll_depth
	global display_string
	# Calculate maximum scroll depth based on display_string length
	if scroll_depth > (len(display_string) / lcd_columns) - lcd_rows:
		scroll_depth = 0
	else:
		scroll_depth += 1

# Set up GPIO for scrolling
scroll_button = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(scroll_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(scroll_button, GPIO.FALLING, callback=scroll, bouncetime=300)

forecast = Forecast()

try:
	while(True):
		forecast_data = forecast.get_forecast_data()
		
		display_string = time.asctime(time.localtime(time.time()))[0:lcd_columns]
		
		if forecast_data:
			temps = [x.get("temperature") for x in forecast_data.get("hourly", {}).get("data", [])[:16]]
			display_string += str(int(max(temps))) + "C / " + str(int(min(temps))) + "C"
			display_string += " "
			display_string += forecast_data.get("currently", {}).get("summary", []) 
			display_string += ". "
			display_string += forecast_data.get("hourly", {}).get("summary", [])
		else:
			display_string += "No forecast data"


		lcd.message(format_for_LCD(display_string))
		
		time.sleep(0.1)

except KeyboardInterrupt:
	print("\nexiting...")
