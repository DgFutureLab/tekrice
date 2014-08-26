import unittest
import app

class DatabaseTests(unittest.TestCase):

	def setUp(self):
		app.database.recreate()

	def test_database_empty_after_recreate(self):
		models = app.database.get_defined_models()
		print models
		# self.assertTrue(len(app.Node.query.all) == 1)

if __name__ == "__main__":
	models = app.database.get_defined_models()
	print models