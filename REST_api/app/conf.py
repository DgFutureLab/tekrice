def config_production(flapp):
	flapp.config.update(
			DEBUG = False,
			PROPAGATE_EXCEPTIONS = False,
			HOST = 'http://107.170.251.142',
			PORT = '80',
			SQLALCHEMY_DATABASE_URI = "postgresql://halfdan:halfdan@localhost/tekrice_prod"
		)

def config_development(flapp):
	flapp.config.update(
			DEBUG = True,
			PROPAGATE_EXCEPTIONS = True,
			HOST = 'http://120.0.0.1',
			PORT = '8080',
			SQLALCHEMY_DATABASE_URI = "postgresql://halfdan:halfdan@localhost/tekrice_dev",
			CSRF_ENABLED = True,
			SECRET_KEY = 'you-will-never-guess'
		)
