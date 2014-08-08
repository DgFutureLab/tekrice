from flask import Flask
import flask_rest
flapp = Flask(__name__)


### Use Twitter Bootstrap
from flask_bootstrap import Bootstrap
Bootstrap(flapp)


### Restify the app
from flask.ext import restful
rest_api = restful.Api(flapp)


### Adds websocket to app
from flask.ext.socketio import SocketIO
socketio = SocketIO(flapp)


### Import modules containing statements that must be executed when the webapp is started (such as adding routes for the REST api)
from app import views, conf, api_core
