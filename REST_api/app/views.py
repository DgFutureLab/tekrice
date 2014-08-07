# coding: utf-8
from app import flapp, socketio
from flask import render_template, request
import time
import json
@flapp.route('/')
def static_wall():
	return render_template('index.html')

@flapp.route('/update_temperature', methods = ['GET', 'POST'])
def store_temperature():
	socketio.emit('new serial data', {'temperature': format_data(json.loads(request.data))}, namespace = '/serial')
	return 'OK'

@socketio.on('request serial data', namespace = '/serial')
def send_images():
	flapp.logger.debug('Got images request in namespace: grid')

def format_data(sensor_data):

	sensor_data = map(lambda s: dict(zip(['time', 'addr', u'reading(°C)'], s.split(','))), sensor_data)
	# sensor_data = map(lambda row: row.update({'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row['time'])))}), sensor_data)
	sensor_data = map(lambda d: ', '.join(['%s: %s'%(k,v) for k,v in d.items()]), sensor_data)
	return sensor_data