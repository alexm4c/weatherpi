#!/usr/bin/python


# specify a list of routes for each combination of incoming 
# request and request type (GET or POST).
# This should direct to a valid module::functionname

# functions that are associated with POST request types should 
# expect to get a single parameter - a dictionary full of values
# filled in from the original form

#--------------------------------
def routes():
	
	routes = (
		{'http_method': 'get', 'path': '/', 'module': 'pages', 'method': 'home'},
		{'http_method': 'post', 'path': '/', 'module': 'pages', 'method': 'submit'})

	return routes