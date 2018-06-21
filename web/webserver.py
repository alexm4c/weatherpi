#!/usr/bin/python
#!/usr/bin/env python

# this finds a matching GET/POST module/function to dispatch to
# based on a list of routes (declared in the routes file)

import sys
import importlib
import cgi
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer

from routes import routes

PORT_NUMBER = 8080
ASSETS_DIR = "assets"

def get_controller(http_method, path):
	for route in routes():	
		if route['http_method'].lower() == http_method.lower() and route['path'].lower() == path.lower():
			module_name = route['module']
			method_name = route['method']
			break
	else:
		raise ValueError
	
	module = importlib.import_module(module_name)
	method = getattr(sys.modules[module_name], method_name)
	return method

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		is_asset = False
		
		try:
			send_reply = False

			if self.path.endswith(".html") or self.path.endswith("/"):
				mimetype = 'text/html'
				send_reply = True

			elif self.path.endswith(".jpg"):
				mimetype = 'image/jpg'
				send_reply = True
				is_asset = True
			
			elif self.path.endswith(".png"):
				mimetype = 'image/png'
				send_reply = True
				is_asset = True
			
			elif self.path.endswith(".gif"):
				mimetype = 'image/gif'
				send_reply = True
				is_asset = True
				
			elif self.path.endswith(".js"):
				mimetype = 'application/javascript'
				send_reply = True
				is_asset = True
				
			elif self.path.endswith(".css"):
				mimetype = 'text/css'
				send_reply = True
				is_asset = True

			if send_reply:
				self.send_response(200)
				self.send_header('Content-type', mimetype)
				self.end_headers()
				if is_asset:
					asset_path = curdir + sep + ASSETS_DIR + sep + self.path
					with open(asset_path, 'rb') as file:
						self.wfile.write(file.read())

				else:					
					method = get_controller('GET', self.path)
					self.wfile.write(bytes(method(), 'utf8'))

		except IOError:
			self.send_error(404, 'File not found: {}'.format(self.path))

		# except ValueError as e:
		# 	print(str(e))
		# 	self.send_error(404, 'Page not found: {}'.format(self.path))

	def do_POST(self):
		form = cgi.FieldStorage(
			fp = self.rfile, 
			headers = self.headers,
			environ = {'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': 'Content-Type'},
			keep_blank_values = True)
		
		parameters = {}
		
		for key in form.keys():
			parameters[key] = form[key].value
		
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		
		method = get_controller('POST', self.path)
		self.wfile.write(bytes(method(parameters), 'utf8'))

try:
	server = HTTPServer(('', PORT_NUMBER), Handler)
	server.serve_forever()
	
except KeyboardInterrupt:
	print('exiting...')

finally:
	server.socket.close()
	