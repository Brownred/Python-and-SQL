import unittest
import sys
sys.path.append('..')

from db_connection import Connect

# from BikeRentals.db_connection import Connect

class TestDatabaseConnection(unittest.TestCase):
    def test_create_table(self):
        with Connect() as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test_table (id serial PRIMARY KEY, name VARCHAR(20));")
            conn.commit()
            cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = 'test_table';")
            result = cursor.fetchone()
            cursor.close()
            self.assertIsNotNone(result)
            
    def test_insert_data(self):
        with Connect() as conn:
            cursor = conn.connect()
            cursor.execute("INSERT INTO test_table (name) VALUES ('Jon Doe');")
            conn.commit()
            cursor.execute("SELECT * FROM test_table WHERE name='Jon Doe';")
            result = cursor.fetchone()
            cursor.close()
            self.assertIsNotNone(result)
            
    def test_update_data(self):
        with Connect() as conn:
            cursor = conn.connect()
            cursor.execute("UPDATE test_table SET name='Jane Doe' WHERE name='Jon Doe';")
            conn.commit()
            cursor.execute("SELECT * FROM test_table WHERE name='Jane Doe';")
            result = cursor.fetchone()
            cursor.close()
            self.assertIsNotNone(result)
            
    def test_delete_data(self):
        with Connect() as conn:
            cursor = conn.connect()
            cursor.execute("DELETE FROM test_table WHERE name='Jane Doe';")
            conn.commit()
            cursor.execute("SELECT * FROM test_table WHERE name='Jane Doe';")
            result = cursor.fetchone()
            cursor.close()
            self.assertIsNone(result)
    
    def test_drop_table(self):
        with Connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE test_table;")
            conn.commit()
            cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = 'test_table';")
            result = cursor.fetchone()
            cursor.close()
            self.assertIsNone(result)
            
if __name__ == "__main__":
    unittest.main()
            