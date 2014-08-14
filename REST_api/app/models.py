from database import Base, db_session
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import uuid

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
	uuid = Column( String(), unique = True )
	alias = Column( String(100) )
	location = Column( String(100) )
	
	sensors = relationship('Sensor', backref = 'node')

	def __init__(self, **kwargs):
		if kwargs.has_key('uuid'): 
			self.uuid = kwargs['uuid']
		else:
			self.uuid = uuid.uuid4()

		if kwargs.has_key('location'): 
			self.location = kwargs['location']

		if kwargs.has_key('alias'): 
			self.alias = kwargs['alias']

@create
class Sensor(Base):
	__tablename__ = 'sensors'
	
	id = Column( Integer, primary_key = True )
	uuid = Column( String(), unique = True )
	unit = Column( String() )

	node_id = Column( Integer, ForeignKey('nodes.id') )
	readings = relationship('Reading', backref = 'sensor')

	def __init__(self, **kwargs):
		if kwargs.has_key('uuid'): 
			self.uuid = kwargs['uuid']
		else:
			self.uuid = uuid.uuid4()
		if kwargs.has_key('unit'): 
			self.unit = kwargs['unit']

	

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

	def __init__(self, timestamp, value):
		self.timestamp 
		







