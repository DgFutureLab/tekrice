from datetime import datetime

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


class SensorReading:
	""" 
	Rudimentary data model for sensor data 
	"""

	def __init__(self, value, unit, timestamp):
		assert isinstance(value, int or float)
		assert isinstance(value, Unit)
		assert isinstance(timestamp, datetime)
		self.value = value
		self.unit = unit
		self.timestamp = timestamp

	def convert_to_unit(self, new_unit, inplace = False):
		pass
