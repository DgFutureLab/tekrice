import unittest
from tests import *
import app
import inspect
import sqlalchemy



if __name__ == "__main__":
	app.conf.config_test_env(app.flapp)


	unittest.main()