from flask import Flask
flapp = Flask(__name__)

from flask.ext.socketio import SocketIO
socketio = SocketIO(flapp)

from app import views, conf