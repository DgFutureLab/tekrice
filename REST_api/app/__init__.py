from flask import Flask
flapp = Flask(__name__)

from flask_bootstrap import Bootstrap
Bootstrap(flapp)

from flask.ext.socketio import SocketIO
socketio = SocketIO(flapp)

from app import views, conf