import unittest
from datetime import datetime, timedelta
from BikeRentals.bike_rentals import BikeRental, customer_info

class TestBikeRental(unittest.TestCase):
    def setUp(self):
        self.shop1 = BikeRental()
        self.shop2 = BikeRental(10)
        
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
        self.assertEqual(self.shop2._rentBikeOnDailylyBasis(-1), None)
        
    def test_rentBikeOnDailyBasis_for_zero_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(0), None)
        
    def test_rentBikeOnDailyBasis_for_valid_positive_number_of_bikes(self):
        now = datetime.datetime.now()
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(2).now, now)
        
    def test_rentBikeOnDailyBasis_for_valid_positive_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(11), None)
      
        
    # Tests on Daily Basis
    def test_rentBikeOnDailylyBasis_for_negative_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnDailylyBasis(-1), None)
        
    def test_rentBikeOnDailyBasis_for_zero_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(0), None)
        
    def test_rentBikeOnDailyBasis_for_valid_positive_number_of_bikes(self):
        now = datetime.datetime.now()
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(2).now, now)
        
    def test_rentBikeOnDailyBasis_for_valid_positive_number_of_bikes(self):
        self.assertEqual(self.shop2._rentBikeOnDailyBasis(11), None)    