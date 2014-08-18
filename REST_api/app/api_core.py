from datetime import datetime
from app import rest_api
import json
from flask.ext import restful
from flask import request
from app.models import Node, Sensor, Reading

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

class NodeResource(restful.Resource):
	def get(self, uid):
		node = Node.query.filter_by(uuid = uid).first()
		return {}

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

		# return json.dumps({'value':self.value, 'unit': repr(self.unit), 'timestamp': self.timestamp})
	
rest_api.add_resource(SensorResource, '/sensor/<string:sensor_type>')



