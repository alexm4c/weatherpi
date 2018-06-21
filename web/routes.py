#!/usr/bin/python

def routes():
	
	routes = (
		{'http_method': 'get', 'path': '/', 'module': 'pages', 'method': 'home'},
		{'http_method': 'post', 'path': '/', 'module': 'pages', 'method': 'submit'})

	return routes