import serial
import os
import re
import requests
import time
import sys
from Queue import Queue, Full
from threading import Thread, Event
from logging import Logger, Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
from argparse import ArgumentParser
from datetime import datetime
import zlib
import json

logger = Logger(__name__)
filehandler = RotatingFileHandler('log.txt', maxBytes = 10**6)
streamhandler = StreamHandler(sys.stdout)
formatter = Formatter('%(asctime)s - %(thread)d - %(levelname)s - %(message)s')
filehandler.setFormatter(formatter)
streamhandler.setFormatter(formatter)
logger.addHandler(filehandler)
logger.addHandler(streamhandler)



def open_serial_device():
	try:
		device = '/dev/' + filter(lambda x: re.match('tty.usb*', x) or re.match('ttyUSB*', x), os.listdir('/dev'))[0]
		serial_device = serial.Serial(device, BAUDRATE, timeout = 5)
		logger.debug('Opening device %s'%device)
		return serial_device
	except IndexError:
		logger.fatal("Couldn't find any Arduino devices. Are you sure it's plugged in? :)")
		os._exit(1)
		

def parse_reading(reading):
	try:
		addr, payload = reading.split('@')
		addr = addr[1:]
		parsed = map(lambda y: dict(zip(['alias', 'value', 'timestamp'], y)), map(lambda x: x.split(':'), payload[:-3].split(';')))
		for p in parsed: 
			p.update({'node_id':addr})
			p.update({'timestamp':datetime.now().strftime('%Y-%m-%d-%H:%M:%S:%f')})
		return parsed 
	except ValueError:
		logger.exception('Recieved garbage from serial port: %s'%reading)
		return []
	


def read_serial(name, is_running):
	logger.debug('Running %s daemon'%name)
	serial_connection = open_serial_device()
	previous_reading = ''

	while is_running.isSet():
		try:
			reading = serial_connection.readline()
			logger.debug('From serial: %s'%reading)
		except ValueError:
			message = 'Problem reading serial port. Please try to run the program again!'	
			logger.fatal(message)
			os._exit(1)

		### If the current reading is the same as the previous reading, there is no reason to send it to the Internet
		if reading != previous_reading:
			previous_reading = reading
			parsed_reading = parse_reading(reading)
			for i, p in enumerate(parsed_reading):
				try:
					queue.put_nowait(p)
				except Full:
					for i in range(10):
						discarded_reading = queue.get_nowait()
					queue.put_nowait(p)
					try:
						logger.warning('Full queue. Discarding data: %s'%(queue.qsize(), discarded_reading))
					except TypeError:
						logger.warning('Full queue. Discarded old data.')
					
		
		logger.debug('Data from serial: %s'%reading)
		time.sleep(0.1)
	
	serial_connection.close()


def upload_daemon(name, is_running):
	logger.debug('Running %s daemon'%name)
	while is_running.isSet():
		if not queue.empty():
			request_payload = prepare_data_in_queue()
			compressed_payload = compress_data(request_payload)
			try:
				response = requests.post(URL, data = compressed_payload)
				logger.info('Sent %s bytes of data and got response: %s'%(sys.getsizeof(compressed_payload), response))
			except requests.ConnectionError:
				logger.warning('Could not connect to host. Discarding data: %s'%request_payload)
			finally:
				response.close()
		
		time.sleep(UPLOAD_INTERVAL)


def compress_data(json_data):
	return zlib.compress(json.dumps(json_data))


def prepare_data_in_queue():
	request_payload = list()
	for i in range(queue.qsize()):
		reading =  queue.get_nowait()
		try:
			d = {'value' : reading['value'], 'timestamp' : reading['timestamp']}
		except KeyError, e:
			logger.exception(e)
		request_payload.append(d)
	return request_payload


def get_url(node_id, sensor_alias):
	return 'http://%s:%s/reading/node_%s/%s'%(HOST, PORT, node_id, sensor_alias)

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('--host', help = 'Server IP address e.g., 107.170.251.142', default = '127.0.0.1')
	parser.add_argument('--port', help = 'Port on the server', default = 8080)
	parser.add_argument('-b', '--baud', help = 'Serial port baud rate (default 57600)', default = 57600)
	parser.add_argument('-q', '--queue_size', help = 'The size of the queue that functions as a buffer between Serial-to-Internet', default = 100)
	parser.add_argument('-u', '--upload_interval', help = 'Interval in seconds (can be float) between uploading to the server', default = 1)
	parser.add_argument('-d', '--debug_level', help = 'Port on the server', default = 'INFO')

	args = parser.parse_args()

	try:
		QUEUE_MAXSIZE = int(args.queue_size)
	except ValueError:
		logger.critical("Please specify an integer for the queue size")
		os._exit(1)

	HOST = args.host
	
	try:
		PORT = int(args.port)
	except ValueError:
		logger.critical("Please specify a port with an integer")
		os._exit(1)

	try:	
		BAUDRATE = int(args.baud)
	except ValueError:
		logger.critical("Please specify the baudrate of the serial port with an integer")
		os._exit(1)

	try:
		UPLOAD_INTERVAL = int(args.upload_interval)
	except ValueError:
		logger.critical("Please specify the the number of seconds to wait between uploading data to the host as an integer")
		os._exit(1)

	try:
		logger.setLevel(args.debug_level)	
	except ValueError:
		logger.critical("Please specify a valid debug level (DEBUG, INFO, WARNING, etc.)")
		os._exit(1)


	URL = 'http://%s:%s/reading/batch'%(HOST, PORT)

	queue = Queue(QUEUE_MAXSIZE)
	
	logger.info('*******************************************************\n')
	logger.info('Process id: %s', os.getpid())
		
	is_running = Event()
	is_running.set()
	
	serial_reader = Thread(target = read_serial, args = ('Serial reader', is_running), name = 'SERIAL READER')
	serial_reader.start()

	if args.host:
		uploader = Thread(target = upload_daemon, args = ('Data sender', is_running), name = 'UPLOADER')
		uploader.start()
	else:
		logger.warning('ATTENTION: Running without remote host, so no data is being sent to server')
	
	try:
		while True:
			time.sleep(0.1)
	except KeyboardInterrupt:
		is_running.clear()
		serial_reader.join()

