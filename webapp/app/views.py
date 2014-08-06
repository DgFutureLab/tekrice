from app import flapp, socketio
from flask import render_template, request

@flapp.route('/')
def static_wall():
	return render_template('index.html')

@flapp.route('/color', methods = ['GET', 'POST'])
def send_color():
	color = request.data
	print color
	socketio.emit('new serial data', {'color':color}, namespace = '/serial')
	return 'OK'

@socketio.on('request serial data', namespace = '/serial')
def send_images():
	flapp.logger.debug('Got images request in namespace: grid')
