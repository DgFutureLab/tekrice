def config_production(flapp):
	flapp.config.update(
			DEBUG = False,
			PROPAGATE_EXCEPTIONS = False,
			HOST = 'http://107.170.251.142',
			PORT = '80'
		)

def config_development(flapp):
	flapp.config.update(
			DEBUG = True,
			PROPAGATE_EXCEPTIONS = True,
			HOST = 'http://120.0.0.1',
			PORT = '8080'
		)

