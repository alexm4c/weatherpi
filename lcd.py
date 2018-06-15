#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD

# LCD pin configuration
RS = 27
EN = 22
D4 = 25
D5 = 24
D6 = 23
D7 = 18

# LCD dimensions
COLUMNS = 20
ROWS = 4

class LCD(Adafruit_CharLCD):
	def __init__(self):
		super().__init__(RS, EN, D4, D5, D6, D7, COLUMNS, ROWS)
		# self.display_string = ''
		# self.scroll_depth = 0

	def message(self, string):
		# Slice a message exactly as long as the LCD has characters beginning at the scroll_depth-th row
		# string = string[scroll_depth*COLUMNS:scroll_depth*COLUMNS+(COLUMNS*ROWS)]
		string = string.replace('\n', '')
		string = string.replace('\r', '')
		string = string.ljust(COLUMNS*ROWS)
		string = string[:COLUMNS*ROWS]
		string = '\n'.join([string[i:i+COLUMNS] for i in range(0, len(string), COLUMNS)])
		super().message(string)

	# def scroll(channel):
	# 	if scroll_depth > (len(display_string) / COLUMNS) - ROWS:
	# 		scroll_depth = 0
	# 	else:
	# 		scroll_depth += 1
