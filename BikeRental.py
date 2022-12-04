import datetime
#Inorder to connect to a PostgreSQL database instance use the psycopg2 library
import psycopg2

class customer_info:
    def __init__(self, ID, fisrt_Name, Last_name, Address, Contact_info, Age:int):
        
        """
        Our constructor method which allows for saving of individual customer infomation to a csv file, "Bike_rental_Customer_info.csv"
        """
        
        self.ID = ID
        self.first_name = fisrt_Name
        self.Last_name = Last_name
        self.Address = Address
        self.contact_info = Contact_info
        self.Age = Age
        
        # Creating a connection object
        conn = psycopg2.connect(database = "BikeRentalsDatabase",
                        host = "127.0.0.1",
                        user = "postgres",
                        password = "denji",
                        port = "5432")
        
        # creating a Cusor object to help execute queries
        self.cursor = conn.cursor()
        
        # Insert the customer details into the databse
        self.cursor.execute("INSERT INTO Customer_Data (Name,address) VALUES (%s,%s)",(self.first_name, self.Address))
        

class BikeRental:
    def __init__(self, stock=int(100)):
        """
        constructor class that instantiates bike rental shop.
        """
        self._stock = stock
        
    # Try rectify return bike bug
    def returnStock(self):
        return self._stock
        
    def displaystock(self):
        """
        Displays the bikes currently available for rent in the shop.
        """
        
        print(f"We currently have {self._stock} bikes available to rent.")
        
    def _rentBikeOnHourlyBasis(self, n):
        """
        Rent bike on hourly basis to a customer.
        Implement a default time period of an hour if the time spent is less than an hour.
        """
        now = datetime.datetime.now()
        print(f"You have rented {n} bike(s) on hourly basis on {now.date()} at {now.time()} hours.")
        print("You will be charged $5 for each hour per bike.")
        print("We hope that you enjoy our service.")
            
        self._stock -= n

        if now:   
            self._rentalTime = now
        else:
            self._rentalTime = 1
        #return now
    
    def _rentBikeOnDailyBasis(self, n):
        """
        rent bike on daily basis to a customer.
        """
            
        now = datetime.datetime.now()
        print(f"You have rented {n} bike(s) on daily basis on {now.date()} at {now.time()} hours.")
        print("You will be charged $20 for each day per bike.")
        print("We hope that you enjoy our service.")
            
        self._stock -= n
            
        if now:   
            self._rentalTime = now
        else:
            self._rentalTime = 1
        #return now
        
    def _rentBikeOnWeeklyBasis(self, n):
        """
        Rent bike on hourly basis to a customer.
        """
            
        now = datetime.datetime.now()
        print(f"You have rented {n} bike(s) on weekly basis on {now.date()} at {now.time()} hours.")
        print("You will be charged $60 for each week per bike.")
        print("We hope that you enjoy our service.")
            
        self._stock -= n

        if now:   
            self._rentalTime = now
        else:
            self._rentalTime = 1
        #return now
        
    def returnBike(self, request):
        """
        1. Accept a rented bike from a customer.
        2. Replenishes the inventory.
        3. Return a bill
        """
        
        # extract the tuple and initiate the bill
        rentalTime, rentalBasis, numOfBikes = request
        bill = 0
        
        # issue a bill only if all three parameters are not null!
        if rentalTime and rentalBasis and numOfBikes:
            self._stock += numOfBikes
            now = datetime.datetime.now()
            rentalPeriod = now - rentalTime
            
            # hourly bill calculation
            if rentalBasis == 1:
                bill = round(rentalPeriod.seconds /3600) * 5 * numOfBikes
            
            # daily bill calculation
            elif rentalBasis == 2:
                bill = round(rentalPeriod.days) * 20 * numOfBikes
                
            # weekly bill calculation
            elif rentalBasis == 2:
                bill = round(rentalPeriod.days /7) * 60 * numOfBikes
                
            # family discount calculation
            if (3 <= numOfBikes <= 5):
                print("You are eligible for family rental promotion of 30% discount")
                bill = bill * 0.7
                
            print("Thanks for returning your bike. Hope you enjoyed our services!")
            print(f"That would be ${bill}")
            return bill
        
        else:
            print("Are you sure you rented a bike with us? If so enter the correct rentalPeriod and basis and numberOfBikes")
            return None
    
class customer(BikeRental, customer_info):
    def __init__(self):
        #Add a custom exception to prevent any usage of this or any class before customer info is entered, Only allows for bike retrun
        
        """
        Our constructor method which instantiates various customer objects.
        """

        super().__init__(self)
        
        self._bikes = 0
        self._rentalBasis = 0
        self._bill = 0
        self._rentalTime = 0
        
    def requestBike(self):
        """
        Takes a request from the customer for the number of bikes.
        """
        
        
        # implement a logic for invalid input
        try:
            self._bikes = int(input("How many bikes would you like to rent: "))
        except ValueError:
            print("That's not a positive integer")
            return -1
        
        if self._bikes < 1:
            print("Invalid input. Number of bikes should be greater than zero!")
            return -1
    
        # do not rent bike if stock is less than requested bikes
#--->>  #elif self._bikes > super().returnStock(): \\Error Tot solve
            #print(f"Sorry! We have currently {self._stock} bikes available to rent.")
            #return None
        else:
            #self._bikes = bikes
            
            rental_basis = int(input("Enter your Rental Basis: "))
            
            match rental_basis:
                case 1:
                    BikeRental()._rentBikeOnHourlyBasis(self._bikes)
                    self._rentalBasis = 1
                    print("Your Have chosen hourly rental basis")
                case 2:
                    BikeRental()._rentBikeOnDailyBasis(self._bikes)
                    self._rentalBasis = 2
                    print("Your Have chosen daily rental basis")
                case 3:
                    BikeRental()._rentBikeOnWeeklyBasis(self._bikes)
                    self._rentalBasis = 3
                    print("Your Have chosen weekly rental basis")

            
            # Brush up on this
            self.cursor.execute("INSERT INTO Customer_Data (Name,address) VALUES (%s,%s)",(self._rentalBasis, self._bikes))
        
    def returnBike(self):
        """
        Allows customers to return their bikes to rental shop.
        """
        
        if self._rentalBasis and self._rentalTime and self._bikes:
            super().returnBike((self._rentalTime, self._rentalBasis, self._bikes))
            #return (self._rentalTime, self._rentalBasis, self._bikes)
        else:
            #Id = int(input("Input Customer's ID"))
            #Search for the customers id in rental information if none ...
            return self._rentalTime, self._rentalBasis, self._bikes

# Error Self._bikes not setting itself to desired values,, check why

