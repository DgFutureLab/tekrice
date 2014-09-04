import serial
import os
import re
import requests
import time
import sys
from Queue import Queue, Empty, Full
from threading import Thread, Event
from logging import Logger, Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
from argparse import ArgumentParser


logger = Logger(__name__)

filehandler = RotatingFileHandler('log.txt', maxBytes = 10**6)
streamhandler = StreamHandler(sys.stdout)
formatter = Formatter('%(asctime)s - %(thread)d - %(levelname)s - %(message)s')
filehandler.setFormatter(formatter)
streamhandler.setFormatter(formatter)
logger.addHandler(filehandler)
logger.addHandler(streamhandler)

parser = ArgumentParser()
parser.add_argument('--host', help = 'Server IP address e.g., 107.170.251.142', default = '127.0.0.1')
parser.add_argument('--port', help = 'Port on the server', default = 8080)
parser.add_argument('-b', '--baud', help = 'Serial port baud rate (default 57600)', default = 57600)
parser.add_argument('-q', '--queue_size', help = 'The size of the queue that functions as a buffer between Serial-to-Internet', default = 100)
parser.add_argument('-u', '--upload_interval', help = 'Interval in seconds (can be float) between uploading to the server', default = 1)
parser.add_argument('-d', '--debug_level', help = 'Port on the server', default = 'INFO')

args = parser.parse_args()
logger.setLevel(args.debug_level)
queue = Queue(100)

def open_serial_device():
	try:
		device = '/dev/' + filter(lambda x: re.match('tty.usb*', x), os.listdir('/dev'))[0]
		serial_device = serial.Serial(device, args.baud, timeout = 5)
		logger.debug('Opening device %s'%device)
		return serial_device
	except IndexError:
		logger.fatal("Couldn't find any arduino devices. Are you sure it's plugged in? :)")
		os._exit(1)
		


def with_timestamp(message):
	return str(time.time()) + ',' + message


def parse_reading(reading):
	try:
		addr, payload = reading.split('@')
		addr = addr[1:]
		parsed = map(lambda y: dict(zip(['alias', 'value', 'timestamp'], y)), map(lambda x: x.split(':'), payload[:-3].split(';')))
		for p in parsed: p.update({'node_id':addr})
		return parsed 
	except Exception, e:
		logger.exception(e)
		return []
	


def read_serial(name, is_running):
	logger.debug('Running %s daemon'%name)
	serial_connection = open_serial_device()
	previous_reading = ''

	while is_running.isSet():
		reading = serial_connection.readline()

		try:
			pass
		except ValueError:
			message = 'Problem reading serial port. Please try to run the program again!'	
			print message
			logger.fatal(message)
			os._exit(1)

		### If the current reading is the same as the previous reading, there is no reason to send it to the Internet
		if reading != previous_reading:
			previous_reading = reading
			parsed_reading = parse_reading(reading)
			for p in parsed_reading:
				try:
					queue.put_nowait(p)
				except Full:
					logger.warning('Full queue. Discarding data: %s'%p)
			
		
		logger.debug('Data from serial: %s'%reading)
		time.sleep(0.1)
	
	serial_connection.close()


def upload_daemon(name, is_running):

	logger.debug('Running %s daemon'%name)
	node_id = 1
	while is_running.isSet():
		try:
			data_list = get_data_in_queue()
			for reading in data_list:
				url = 'http://localhost:8080/reading/node/%s/%s'%(reading['node_id'], reading['alias'])
				
				data = {'value' : reading['value'], 'timestamp' : reading['timestamp']}
				response = requests.put(url, data = data)
				logger.info(response.text)
		except Empty:
			pass
		time.sleep(args.upload_interval)


def get_data_in_queue():
	data_list = list()
	while not queue.empty():
		data_list.append( queue.get())
	return data_list


def get_url(node_id, sensor_alias):
	return 'http://%s:%s/%s/%s/'%(args.host, args.port, node, sensor)

if __name__ == "__main__":
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

