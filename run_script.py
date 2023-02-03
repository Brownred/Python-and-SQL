"""
This is where we will run our BikeRentals system.
"""
from BikeRentals.bike_rentals import *
import time
shop1 = BikeRental()
shop1.set_stock(10)

# Enter new customer details
customer1 = customer_info('Pete', 'Paker', 20, 'Male', 1597535248, 'pete@xyz.com', 'California')
customer1.commit_info()

# cust1 = customer()
# cust1.requestBike()
# time.sleep(10)
# cust1.custReturnBike()