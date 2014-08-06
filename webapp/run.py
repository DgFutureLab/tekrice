from app import flapp, socketio
# from threading import Thread


if __name__ == "__main__":
	# Thread(target = read_serial_port).start()
	flapp.config['DEBUG'] = True
	socketio.run(flapp, port = 8080)
