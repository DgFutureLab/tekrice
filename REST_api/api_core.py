from datetime import datetime
from app import rest_api, flapp
import json
from flask.ext import restful
from flask import request
from app.models import Node, Sensor, Reading
from sqlalchemy.exc import IntegrityError

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

class ReadingResource(restful.Resource):

	def put(self, node_uuid, sensor_alias):
		satoyama.add_new_reading(node_uuid, sensor_alias, value, timestamp)



		
		flapp.logger.warning('Received node_uuid: %s, sensor_alias: %s'%(node_uuid, sensor_alias))

		node = Node.query.filter_by(uuid = node_uuid).first()
		flapp.logger.debug(node)
		if node:
			sensor = Sensor.query.filter_by(node = node, alias = sensor_alias)
		else:
			node = Node.create(uuid = node_uuid)
			sensor = Sensor.create(alias = sensor_alias, node = node)

		reading_args = {'sensor':sensor}

		# flapp.logger.debug(node)
		# flapp.logger.debug(sensor)

		try:
			reading_args.update({'timestamp': request.form['timestamp']})
		except KeyError:
			pass
		
		try:
			reading_args.update({'value': request.form['value']})
		except KeyError:
			pass

		# reading = Reading(**reading_args)

		return {'status': 'OK'}
		# if not sensor:
			# sensor = Sensor.create(alias = sensor_alias)
		# node.sensors.append(sensor)


		# return json.dumps({'value':self.value, 'unit': repr(self.unit), 'timestamp': self.timestamp})
	




rest_api.add_resource(SensorResource, '/sensor/<string:sensor_type>')
rest_api.add_resource(ReadingResource, '/reading/<string:node_uuid>/<string:sensor_alias>')


