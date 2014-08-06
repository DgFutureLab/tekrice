from app import flapp, socketio
from flask import render_template, request

@flapp.route('/')
def static_wall():
	return render_template('index.html')

@flapp.route('/update_temperature', methods = ['GET', 'POST'])
def store_temperature():
	temperature = request.data
	print temperature
	socketio.emit('new serial data', {'temperature':temperature}, namespace = '/serial')
	return 'OK'

@socketio.on('request serial data', namespace = '/serial')
def send_images():
	flapp.logger.debug('Got images request in namespace: grid')
