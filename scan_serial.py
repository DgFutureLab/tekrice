import serial
import urllib2
import os
import re
import numpy
import time
import sys
from Queue import Queue, Empty, Full
from threading import Thread, Event
from logging import Logger, Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
from argparse import ArgumentParser
import json

logger = Logger(__name__)
logger.setLevel('DEBUG')
filehandler = RotatingFileHandler('log.txt', maxBytes = 10**6)
streamhandler = StreamHandler(sys.stdout)
formatter = Formatter('%(asctime)s - %(thread)d - %(levelname)s - %(message)s')
filehandler.setFormatter(formatter)
streamhandler.setFormatter(formatter)
logger.addHandler(filehandler)
logger.addHandler(streamhandler)

parser = ArgumentParser()
parser.add_argument('-r', '--remote-host', help = 'Server IP address e.g., 107.170.251.142')
parser.add_argument('-b', '--baud', help = 'Serial port baud rate (default 57600)', default = 57600)
parser.add_argument('-q', '--queue_size', help = 'The size of the queue that functions as a buffer between Serial-to-Internet', default = 100)
parser.add_argument('-u', '--upload_interval', help = 'Interval in seconds (can be float) between uploading to the server', default = 1)
parser.add_argument('-p', '--port', help = 'Port on the server', default = 8080)

args = parser.parse_args()


# 
queue = Queue(100)

def open_serial_device():
	try:
		device = '/dev/' + filter(lambda x: re.match('tty.usb*', x), os.listdir('/dev'))[0]
		serial_device = serial.Serial(device, args.baud, timeout = 5)
		logger.debug('Opening device %s'%device)
		return serial_device
	except IndexError:
		logger.error("Couldn't find any arduino devices. Are you sure it's plugged in? :)")
		os._exit(1)
		


def with_timestamp(message):
	return str(time.time()) + '; ' + message

def read_serial(name, is_running):
	logger.debug('Running %s daemon'%name)
	serial_connection = open_serial_device()
	previous_reading = ''

	while is_running.isSet():
		reading = with_timestamp( serial_connection.readline() )
		try:
			pass
		except ValueError:
			print 'Problem reading serial port. Please try to run the program again!'	
			os._exit(1)

		### If the current reading is the same as the previous reading, there is no reason to send it to the Internet
		if reading != previous_reading:
			try:
				queue.put_nowait(reading)
			except Full:
				logger.warning('Full queue. Discarding reding: %s'%reading)
			previous_reading = reading
		
		logger.debug('Data from serial: %s'%reading)
		time.sleep(0.1)
	
	serial_connection.close()


def upload_daemon(name, is_running):

	logger.debug('Running %s daemon'%name)
	while is_running.isSet():
		try:
			data = get_data_in_queue()
			logger.debug(json.dumps(data))
			request = urllib2.Request(url, data = json.dumps(data), headers = {'Content-Type':'text/plain'})
			response = urllib2.urlopen(request)
			logger.debug(response)
		except Empty:
			pass
		time.sleep(args.upload_interval)

def clean_reading(reading):
	return reading.replace('\n', '').replace('\r', '')

def get_data_in_queue():
	data_list = list()
	while not queue.empty():
		data_list.append( clean_reading(queue.get()))
	return data_list

if __name__ == "__main__":
	logger.info('*******************************************************\n')
	logger.info('Process id: %s', os.getpid())
	
	is_running = Event()
	is_running.set()

	
	serial_reader = Thread(target = read_serial, args = ('Serial reader', is_running))
	serial_reader.start()


	if args.remote_host:
		url = "http://%s:%s/update_temperature"%(args.remote_host, args.port)
		data_sender = Thread(target = upload_daemon, args = ('Data sender', is_running))
		data_sender.start()
	else:
		print 'ATTENTION: Running without remote host, so no data is being sent to server'
	
	try:
		while True:
			time.sleep(0.1)
	except KeyboardInterrupt:
		is_running.clear()
		serial_reader.join()
