from flask import Flask
flapp = Flask('sensor_api')


### Use Twitter Bootstrap
from flask_bootstrap import Bootstrap
Bootstrap(flapp)

### Restify the app
from flask.ext import restful
rest_api = restful.Api(flapp)

from database import db_session

@flapp.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

### Adds websocket to app
from flask.ext.socketio import SocketIO
socketio = SocketIO(flapp)

### Before importing other modules, import and setup run configuration
from app import conf
flapp.config.update(conf.module_config)



import sys
sys.path.append('/Users/halfdan-rump/projects/')
try:
	print 'asdasd'
	from satoyama import database, models
	from satoyama.models import Node, Sensor, SensorType, Reading
except ImportError:
	print 'Please supply path to satoyama module (this is temporary, until satoyama is on PyPI)'


### Import modules containing statements that must be executed when the webapp is started (such as adding routes for the REST api)
import resources
# from app import api_core, loggers