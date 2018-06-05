#!/usr/bin/python
import time
from dark_sky_api import Dark_Sky_API

DISPLAY_WIDTH = 20

def display_string(api):

	forecast_data = api.get_forecast_data()
	
	display_string = time.asctime(time.localtime(time.time()))[0:DISPLAY_WIDTH]

	if forecast_data:
		temps = [x.get("temperature") for x in forecast_data.get("hourly", {}).get("data", [])[0:16]]
		display_string += str(int(max(temps))) + "C / " + str(int(min(temps))) + "C"
		display_string += " "
		display_string += forecast_data.get("currently", {}).get("summary", []) 
		display_string += ". "
		display_string += forecast_data.get("hourly", {}).get("summary", [])
	else:
		display_string += "No forecast data"

	return '\n'.join([display_string[i:i+DISPLAY_WIDTH] for i in range(0, len(display_string), DISPLAY_WIDTH)])


if __name__ == '__main__':
	
	api = Dark_Sky_API()

	while(1):
		print(display_string(api))
		time.sleep(1)