from datetime import datetime
from app import rest_api, flapp
from satoyama.models import Node, Sensor, SensorType, Reading

import json
from flask.ext import restful
from flask import request
from sqlalchemy.exc import IntegrityError, DataError

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
import inspect
class NodeResource(restful.Resource):
	def get(self, uid):
		node = Node.query.filter_by(uuid = uid).first()
		return {'node':node}

	def post(self, uid):
		# print dict(request.form)
		if request.form.has_key('alias'):
			alias = request.form['alias']
			print type(alias)
		
		# try:
		node = Node.create(uuid = uid)
		return {'node': str(node)}
		# return {'node': node.__repr__()}
			# except IntegrityError:
			# 	return {'fukka you!':'node already exists...'}
			# except Exception, e:
			# 	return {'exception':json.dumps(e)}


rest_api.add_resource(NodeResource, '/node/<string:uid>')


class SensorResource(restful.Resource):
	

	def get(self, alias, sensor_type):
		""" 
		REST GET handler. Query database and return json dump of retrieved object(s)
		:param alias: node UUID or alias
		:param sensor_type: 
		"""

		#OPTIONAL SENSOR UUID

		print alias, sensor_type
		node = Node.query.filter_by(alias = alias).first()
		sensors = Sensor.query.filter_by(node_id = node.id, type = sensor_type).all()
		
		if readings.has_key(key):
			return {'value':readings[(alias, sensor_type)]}
		else:
			return {'value': 'EMPTY'}

	def put(self, node, sensor_type):
		readings[(node, sensor_type)] = request.data
		print readings
		return 'OK'

class ApiResponse(object):
	

	def __init__(self, request):
		self.warnings = list()
		self.errors = list()
		self.request_data = request.form
		self.objects = list()

	def add_warning(self, warning):
		self.warnings.append(warning)

	def add_error(self, error):
		self.errors.append(error)

	def add_object(self, obj):
		self.objects.append(obj)

	def json(self):
		return {'warnings': self.warnings, 'errors': self.errors, 'request': self.request_data, 'data': self.objects}


def get_form_data(response, field = None):
	assert isinstance(response, ApiResponse), 'response must an instance of type ApiResponse'
	try:
		field = request.form[field]
	except KeyError:
		response.add_warning('Missing field: %s'%field)
		field = None
	finally:
		return field


class ReadingResource(restful.Resource):

	def get(self, node_id, sensor_alias):
		response = ApiResponse(request)

		node, sensor = None, None

		try:
			node = Node.query.filter_by(id = node_id).first()
		except DataError:
			response.add_error('node_id must be an integer')
		if not node: response.add_error('Insert reading failed: No node with id %s'%node_id)

		try:
			sensor = Sensor.query.filter_by(alias = sensor_alias, node = node).first()
		except DataError:
			response.add_error('sensor_id must an integer')

		 
		if not sensor: 
			response.add_error('Get reading failed: Node has no sensor with alias %s'%sensor_alias)
		else:
			try:
				reading = Reading.query.filter_by(sensor = sensor).all()[-1]
				print reading.json_detailed()
				response.add_object({'value': reading.value})
			except Exception, e:
				response.add_error(e.message)
		return response.json()

		
	
	def put(self, node_id, sensor_alias):
		""" 
		:param node_uuid: uuid of the node
		:param sensor_identifier: Can be either sensor uuid or sensor alias. 
		"""
		response = ApiResponse(request)

		timestamp = get_form_data(response, 'timestamp')
		value = get_form_data(response, 'value')
		node, sensor = None, None

		try:
			node = Node.query.filter_by(id = node_id).first()
		except DataError:
			response.add_error('node_id must be an integer')
		if not node: response.add_error('Insert reading failed: No node with id %s'%node_id)

		try:
			sensor = Sensor.query.filter_by(alias = sensor_alias, node = node).first()
		except DataError:
			response.add_error('sensor_id must an integer')

		 
		if not sensor: 
			response.add_error('Insert reading failed: Node has no sensor with alias %s'%sensor_alias)
		else:
			try:
				Reading.create(sensor = sensor, value = value, timestamp = timestamp)
			except Exception, e:
				response.add_error(e.message)


		return response.json()


### For administration
rest_api.add_resource(SensorResource, '/sensor/<string:sensor_type>')

### For storing/accessing sensor readings
rest_api.add_resource(ReadingResource, '/reading/node_<string:node_id>/<string:sensor_alias>')
# rest_api.add_resource(ReadingResource, '/reading/sensor/<string:sensor_id>')


