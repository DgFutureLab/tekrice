from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import inspect

engine = create_engine('postgresql://halfdan:halfdan@localhost/tekrice_dev', convert_unicode = True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()




def nuke_db():
	import models
	db_session.close()
	Base.metadata.drop_all(bind=engine)

def init_db():
	import models
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
	Base.metadata.create_all(bind=engine)

def recreate():
	nuke_db()
	init_db()


def get_defined_models():
	import models
	import sqlalchemy
	members = dict(inspect.getmembers(models))
	members.pop('Base')
	models = list()
	for name, member in members.items():
		if isinstance(member, sqlalchemy.ext.declarative.api.DeclarativeMeta):
			models.append(member)
	return models


def db_demo():
	from models import Node, Sensor, SensorType, Reading
	from datetime import datetime
	import time
	from random import gauss

	sensortype = SensorType.create(name = 'Qartz thermometer', unit = 'Celcius')
	node = Node.create(alias = 'ricefield1')
	sensor1 = Sensor.create(sensortype = sensortype, node = node, alias = 'CPU temperature')
	sensor2 = Sensor.create(sensortype = sensortype, node = node, alias = 'Ambient air temperature')
	for i in range(5):
		Reading.create(sensor = sensor1, value = gauss(80, 0.1), timestamp = datetime.now())
		time.sleep(0.1)

	for i in range(5):
		Reading.create(sensor = sensor2, value = gauss(25, 0.1), timestamp = datetime.now())
		time.sleep(0.1)

	print
	print 'NODE:\t', node.json_detailed()
	print
	print 'SENSOR1:\t', sensor1.json_detailed()
	print
	print 'SENSOR2:\t', sensor2.json_detailed()

	return node, sensor1, sensor2