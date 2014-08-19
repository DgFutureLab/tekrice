from flask import Flask
flapp = Flask(__name__)


### Use Twitter Bootstrap
from flask_bootstrap import Bootstrap
Bootstrap(flapp)

### Restify the app
from flask.ext import restful
rest_api = restful.Api(flapp)

# ### Create db
# from flask.ext.sqlalchemy import SQLAlchemy
# db = SQLAlchemy(flapp)
# db.init_app(flapp)

from database import db_session
# init_db()

@flapp.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

### Adds websocket to app
from flask.ext.socketio import SocketIO
socketio = SocketIO(flapp)

### Import modules containing statements that must be executed when the webapp is started (such as adding routes for the REST api)
from app import views, conf, api_core, database, models

flapp.config.update(conf.module_config)