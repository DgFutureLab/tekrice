import logging
import os
# from app import __file__ as appfile
from sys import stdout
from app import flapp

flapp.logger.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

filehandler = logging.FileHandler('api.log')
filehandler.setLevel('DEBUG')
filehandler.setFormatter(formatter)
flapp.logger.addHandler(filehandler)





# consolehandler = logging.StreamHandler(stdout)
# consolehandler.setFormatter(formatter)
# consolehandler.setLevel('WARNING')
# logger.addHandler(consolehandler)


### Create logger for database events

# traffic_logger = logging.Logger(name = 'api.traffic')
# traffic_logger.setLevel('INFO')
# traffic_filter = logging.Filter('api.traffic')

# database_logger = logging.Logger(name = 'api.db')
# database_logger.setLevel('INFO')
# database_logger.addFilter(logging.Filter('api.db'))
# database_logger.addHandler(consolehandler)



# traffic_logger.addHandler(streamhandler)
# api_logger.addHandler(streamhandler)

	# handler = logging.FileHandler('f', encoding = 'utf8')
