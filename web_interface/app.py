from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_redis import FlaskRedis

app = Flask(__name__)
redis_store = FlaskRedis(app, decode_responses=True)

@app.route('/')
def index():
	return redirect(url_for('config'))

@app.route('/config', methods=['GET', 'POST'])
def config():

	config_schema = {'api_key': str, 'latitude': float, 'longitude': float, 'refresh_time': int}
	error_msg = ''

	if request.method == 'POST':

		for key, function in config_schema.items():
			try:
				if request.form[key]:
					redis_store.set(key, function(request.form[key]))
			except ValueError:
				error_msg = '{key} must be of type {func}'.format(key=key, func=function)

	configuration = {}
	
	for key, _ in config_schema.items():
		key = redis_store.get(key)
		if key:
			if key == 'api_key':
				# Obsfucate api key
				key = '{:*<{len}.5}'.format(key, len=len(key))
			configuration[key] = key
		else:
			configuration[key] = ''

	
	return render_template('config.html', config=configuration, error=error_msg)

@app.route('/logs')
def logs():
	return render_template('logs.html')