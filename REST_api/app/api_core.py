from datetime import datetime
from app import rest_api
import json
from flask.ext import restful
from flask import request

API_UNITS = {
	'm':'SI meters', 
	's':'SI seconds'
	}

class UnknownUnitException(Exception):
	def __init__(self, supplied_unit):
		super(UnknownUnitException, self).__init__('Bad unit specified: %s'%supplied_unit)

class Unit:
	def __init__(self, unit_string):
		self.unit = unit_string

	def verify_unit(self):
		if not self.unit in API_UNITS.keys() or self.unit not in API_UNITS.values():
			raise UnknownUnitException(self.unit)
	
	def get_unit_name(self):
		return API_UNITS[self.unit]

	def get_unit_description(self):
		pass

	def __repr__(self):
		return str(self.unit)


readings = dict()

class SensorResource(restful.Resource):
	

	def get(self, location, sensor_type):
		""" 
		REST GET handler. Query database and return json dump of retrieved object(s)
		"""
		key = (location, sensor_type)
		if readings.has_key(key):
			return {'value':readings[(location, sensor_type)]}
		else:
			return {'value': 'EMPTY'}

	def put(self, location, sensor_type):
		readings[(location, sensor_type)] = request.data
		print readings
		return 'OK'


		# return json.dumps({'value':self.value, 'unit': repr(self.unit), 'timestamp': self.timestamp})
	
class dataModel:
	def __init__(self, value, unit, timestamp):
		""" 
		Rudimentary data model for sensor data 
		"""
		assert isinstance(value, int or float)
		assert isinstance(value, Unit)
		assert isinstance(timestamp, datetime)
		self.value = value
		self.unit = unit
		self.timestamp = timestamp

	def convert_to_unit(self, new_unit, inplace = False):
		pass

rest_api.add_resource(SensorResource, '/sensors/<string:location>/<string:sensor_type>')

