from database import Base, db_session
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import uuid
from collections import Iterable
import json
from app import flapp

class ExpectedFieldException(Exception):
	def __init__(self, field):
		message = 'Expected keyword for field %s'%field
		super(ExpectedFieldException, self).__init__(message)


def create(model):						### 'create' is the name of the decorator
	@staticmethod	
	def autocommit(*args, **kwargs): 		### Gets arguments for the object to create
		instance = model(*args, **kwargs) 	### Instance is created
		db_session.add(instance)			### ..added to the seesion
		db_session.commit()					### ..inserted to the database
		return instance 					### ..and returned to the caller
	model.create = autocommit 			###	The model class (e.g. Node, Sensor, etc, is given a create method which calls the inner function) 		
	return model						### The decorated model class is returned and replaces the origin model class



@create
class Node(Base):
	
	__tablename__ = 'nodes'
	
	id = Column( Integer, primary_key = True )
	uuid = Column( String(32), unique = True)
	alias = Column( String(100) )
	sensors = relationship('Sensor', backref = 'node')

	def __init__(self, **kwargs):
		if kwargs.has_key('uuid'): 
			self.uuid = kwargs['uuid']
		else:
			self.uuid = uuid.uuid4().hex

		if kwargs.has_key('alias'): 
			self.alias = kwargs['alias']

		if kwargs.has_key('sensors'):
			sensors = kwargs['sensors']
			if isinstance(sensors, Iterable):
				for sensor in sensors:
					self.sensors.append(sensor)
			else:
				self.sensors.append(sensors)

	def json_detailed(self):
		return {'type': '<Node>', 'uuid': self.uuid, 'alias':self.alias, 'sensors': map(lambda s: s.json_summary(), self.sensors)}

	def json_summary(self):
		return {'type': '<Node>', 'uuid': self.uuid, 'alias':self.alias}
	
	def __repr__(self):
		return json.dumps(self.json_summary())


@create
class SensorType(Base):
	__tablename__ = 'sensortypes'

	id = Column( Integer, primary_key = True)
	name = Column( String() )
	unit = Column( String() )
	alias = Column( String() )
	sensors = relationship('Sensor', backref = 'sensortype')

	def __init__(self, **kwargs):
		if kwargs.has_key('name'):
			self.name = kwargs['name']
		else:
			raise ExpectedFieldException('name')
		
		if kwargs.has_key('unit'):
			self.unit = kwargs['unit']
		else:
			raise ExpectedFieldException('unit')

		if kwargs.has_key('alias'):
			self.alias = kwargs['alias']

	def json_detailed(self):
		return {'type': '<SensorType>', 'name': self.name, 'unit': self.unit, 'sensors':map(lambda s: s.json_summary(), self.sensors, 'id': self.id)}

	def json_summary(self):
		return {'type': '<SensorType>', 'name': self.name, 'id': self.id}

	def __repr__(self):
		return json.dumps(self.json_summary())


@create
class Sensor(Base):
	__tablename__ = 'sensors'
	
	id = Column( Integer, primary_key = True )
	uuid = Column( String(32), unique = True )
	alias = Column( String() )

	readings = relationship('Reading', backref = 'sensor')
	node_id = Column( Integer, ForeignKey('nodes.id') )
	sensortype_id = Column( Integer, ForeignKey('sensortypes.id') )
	

	# unit_id = Column( Integer, ForeignKey('sensortypes.id') )

	def __init__(self, **kwargs):
		if kwargs.has_key('uuid'): 
			self.uuid = kwargs['uuid']
		else:
			self.uuid = uuid.uuid4().hex
		
		if kwargs.has_key('alias'):
			self.alias = kwargs['alias']

		if kwargs.has_key('sensortype'): 
			self.unit = kwargs['sensortype']
		else:
			raise ExpectedFieldException('sensortype')

		if kwargs.has_key('node'):
			self.node = kwargs['node']
		else:
			raise ExpectedFieldException('node')

		if kwargs.has_key('readings'):
			readings = kwargs['readings']
			if isinstance(readings, Iterable):
				for reading in readings:
					self.readings.append(reading)
			else:
				self.readings.append(reading)

	# def describe(self):

	# 	return '<Sensor> uuid: %s, alias: %s, node: %s, sensor_type: %s, readings: %s'%(self.uuid, self.alias, self.node, self.sensortype, self.readings)

	def json_detailed(self):
		return {'type': '<Sensor>', 'uuid': self.uuid, 'sensor_type':self.sensortype, 'readings': map(lambda r: r.json_summary(), self.readings)}

	def json_summary(self):
		return {'type': '<Sensor>', 'uuid': self.uuid, 'sensor_type':self.sensortype}
		# return {'type': '<Sensor>', 'uuid': self.uuid, 'node':self.node, 'sensor_type':self.sensortype, 'readings': map(lambda r: r.details(), self.readings)}

 
	def __repr__(self):
		if self.alias == None:
			return json.dumps({'uuid': self.uuid})# '<Sensor> %s'%self.uuid
		else:
			return json.dumps({'alias': self.alias})
			# '<Sensor> %s'%self.alias
		

@create
class Reading(Base):
	__tablename__ = 'readings'

	id = Column( Integer, primary_key = True )
	timestamp = Column( DateTime() )
	value = Column( Float() )

	sensor_id = Column( Integer, ForeignKey('sensors.id') )

	def __init__(self, **kwargs):

		if kwargs.has_key('timestamp'): 
			self.timestamp = kwargs['timestamp']		

		if kwargs.has_key('value'): 
			self.value = kwargs['value']

		if kwargs.has_key('sensor'):
			self.sensor = kwargs['sensor']
		else:
			raise ExpectedFieldException('sensor')

	def json_detailed(self):
		return {'type': '<Reading>', 'value': self.value, 'timestamp': self.timestamp.strftime(flapp.config['DATETIME_FORMAT'])}

	def json_summary(self):
		return {'type': '<Reading>', 'value': self.value, 'id': self.id}

	def __repr__(self):
		return json.dumps(self.json_summary())
#

		








