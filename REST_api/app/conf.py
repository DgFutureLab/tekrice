import os


class BasicConfig():
	
	REDIS_WALL_Q = 'showing'
	REDIS_ALL_Q = 'all'	
	DEBUG = True
	PROPAGATE_EXCEPTIONS = True

	ORIGINAL_IMAGE_DIR = 'app/static/images/original/'
	
	def makedir(self, dir):
		try:
			os.makedirs(dir)
		except OSError:
			pass

	# GRID_NROWS = {200: }

	def __init__(self):
		
		self.QUEUE_DIR = 'app/static/images/uploaded/queue/'
		self.RANDOM_DIR = 'app/static/images/uploaded/random/'
		self.GRID_DIR_WHITE = 'app/static/images/uploaded/grid_white/'
		self.GRID_DIR_BLACK = 'app/static/images/uploaded/grid_black/'
		self.GRID_DIR_SKETCH = 'app/static/images/uploaded/grid_sketch/'
		self.makedir(self.QUEUE_DIR)
		self.makedir(self.RANDOM_DIR)
		self.makedir(self.GRID_DIR_WHITE)
		self.makedir(self.GRID_DIR_BLACK)
		self.makedir(self.GRID_DIR_SKETCH)


		self.RANDOM_REFRESH_RATE = 8
		self.GRID_REFRESH_RATE = 3

		self.N_RANDOM_WALLPICS = 10
		self.N_QUEUE_WALLPICS = 16
		
		self.N_GRID_ROWS = 7
		self.N_GRID_COLUMNS = 10

	def __getitem__(self, item):
		return getattr(self, item)


class Production(BasicConfig):
	HOST = 'http://107.170.251.142'
	PORT = '80'
	def __init__(self, **kwargs):
		BasicConfig.__init__(self, **kwargs)


class Development(BasicConfig):
	HOST = 'http://127.0.0.1'
	PORT = '8080'
	def __init__(self, **kwargs):
		BasicConfig.__init__(self, **kwargs)