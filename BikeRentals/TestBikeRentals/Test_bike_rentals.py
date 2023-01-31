import unittest
from datetime import datetime, timedelta
from BikeRentals.bike_rentals import BikeRental, customer_info, customer
from BikeRentals.constants import database_info
from BikeRentals.db_connection import Connect

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
            
            
class TestCustomer_info(unittest.TestCase):
    pass
class TestBikeRental(unittest.TestCase):
    def setUp(self):
        self.shop1 = BikeRental()
        self.shop2 = BikeRental(10)
        self.customer = customer()
        
    def test_Bike_Rental_Displays_correct_stock(self):
        self.assertEqual(self.shop1.returnStock(), 0)
        self.assertEqual(self.shop2.returnStock(), 10)
        
    # Tests on Hourly Basis    
    def test_rentBikeOnHourlyBasis_for_negative_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnHourlyBasis(-1), None)
        
    def test_rentBikeOnHourlyBasis_for_zero_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnHourlyBasis(0), None)
        
    def test_rentBikeOnHourlyBasis_for_valid_positive_number_of_bikes(self):
        now = datetime.datetime.now().time()
        self.assertEqual(self.shop2._rentBikeOnHourlyBasis(2).now.time(), now)
        
    def test_rentBikeOnHourlyBasis_for_valid_positive_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnHourlyBasis(11), None)
    
        
    # Tests on Daily Basis
    def test_rentBikeOnDailylyBasis_for_negative_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(-1), None)
        
    def test_rentBikeOnDailyBasis_for_zero_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(0), None)
        
    def test_rentBikeOnDailyBasis_for_valid_positive_number_of_bikes(self):
        now = datetime.datetime.now()
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(2).now, now)
        
    def test_rentBikeOnDailyBasis_for_valid_positive_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(11), None)
      
        
    # Tests on Weekly Basis
    def test_rentBikeOnWeeklyBasis_for_negative_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnWeeklyBasis(-1), None)
        
    def test_rentBikeOnWeeklyBasis_for_zero_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnWeeklyBasis(0), None)
        
    def test_rentBikeOnWeeklyBasis_for_valid_positive_number_of_bikes(self):
        now = datetime.datetime.now()
        self.assertEqual(self.shop2._rentBikeOnWeeklyBasis(2).now, now)
        
    def test_rentBikeOnWeeklyBasis_for_valid_positive_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnWeeklyBasis(11), None)   
        
    
    def test_returnBike_for_invalid_rentalTime(self):
        request = self.customer.returnBike()
        self.assertIsNone(self.shop2.returnBike(request))
        
        # Manually check return func with error values
        self.assertIsNone(self.shop2.returnBike(request))
        
    def test_returnBike_for_invalid_rentalBasis(self):
        # Create a valid rentalTime and bikes
        self.customer._rentalTime = datetime.now()
        self.customer._bikes = 3
        
        # Create invalid rentalBasis
        self.customer._rentalBasis = 7
        
        request =  self.customer.returnBike()
        self.assertEqual(self.shop2.returnBike(request), 0)
        
        
    def test_returnBike_for_invalid_numOfBikes(self):
        # Create a valid rentalTime and rentalBasis
        self.customer._rentalTime = datetime.now()
        self.customer._rentalBasis = 1
        
        # Create invalid bikes
        self.customer._bikes = 0
        
        request =  self.customer.returnBike()
        self.assertIsNone(self.shop2.returnBike(request))
        
    def test_returnBike_for_valid_credentials(self):
        pass
    
    
class TestCustomer(unittest.TestCase):
    
    def test_return_bike_with_valid_input(self):
        pass
        
        