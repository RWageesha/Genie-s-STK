# test/test_connections.py

import unittest
from data.db_config import engine
from data.models import Base
from sqlalchemy import inspect

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        # Create tables
        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        # Drop tables
        Base.metadata.drop_all(bind=engine)

    def test_database_connection(self):
        # Test if tables are created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        self.assertIn("products", tables)
        self.assertIn("batches", tables)
        self.assertIn("sale_records", tables)
        self.assertIn("suppliers", tables)
        self.assertIn("orders", tables)
        self.assertIn("order_items", tables)

if __name__ == '__main__':
    unittest.main()
