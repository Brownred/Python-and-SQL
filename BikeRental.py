import datetime
import psycopg2
#Inorder to connect to a PostgreSQL database instance use the psycopg2 library

class customer_info:
    def __init__(self, ID, Fisrt_Name, Last_name, Age, Gender, Phone_no, email, Location):
        
        """
        Our constructor method which allows for saving of individual customer infomation to a csv file, "Bike_rental_Customer_info.csv"
        """
        
        self.ID = ID
        self.First_name = Fisrt_Name
        self.Last_name = Last_name
        self.Gender = Gender
        self.Phone_no = Phone_no
        self.Age = Age
        self.email = email
        self.Location = Location
        
        # Creating a connection object
        conn = psycopg2.connect(database = "BikeRentalsDatabase",
                        host = "127.0.0.1",
                        user = "postgres",
                        password = "denji",
                        port = "5432")
        
        # creating a Cusor object to help execute queries
        self.cursor = conn.cursor()
        
        # Insert the customer details into the databse by passing the data to fill the placeholders
        try:
            self.cursor.execute("INSERT INTO customer (First_name, Last_name, Age, Gender, Phone_no, email, Location) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                            (self.First_name, self.Last_name, self.Age, self.Gender, self.Phone_no, self.email, self.Location))
        except:
            print("Some Wrong value has been Input")
        else:
            #make changes to the database persistent
            conn.commit()
        
class BikeRental():
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
            return self._rentalTime
        else:
            self._rentalTime = 1
            return self._rentalTime
    
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
            return self._rentalTime
        else:
            self._rentalTime = 1
            return self._rentalTime
        
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
            return self._rentalTime
        else:
            self._rentalTime = 1
            return self._rentalTime
        
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
            
            match rentalBasis:
                # hourly bill calculation
                case 1:
                    bill = round(rentalPeriod.seconds /3600) * 5 * numOfBikes
                    # if bike was rented for less than an hour
                    if bill == 0:
                        bill = 5
                        
                # daily bill calculation
                case 2:
                    bill = round(rentalPeriod.days) * 20 * numOfBikes
                    # if bike was rented for less than an day period
                    if bill == 0:
                        bill = 10
                        
                # weekly bill calculation
                case 3:
                    bill = round(rentalPeriod.days /7) * 60 * numOfBikes
                    # if bike was rented for less than an week period
                    if bill == 0:
                        bill = 60
                    
            # family discount calculation
            if (3 <= numOfBikes <= 5):
                print("You are eligible for family rental promotion of 30% discount")
                bill = bill * 0.7
            
            name = input("Enter Last_name only again \n")
            bike_Condition = input("What is(are) the condition(s) of the bikes? \n")
        
            # Creating a connection object
            conn = psycopg2.connect(database = "BikeRentalsDatabase",
                        host = "127.0.0.1",
                        user = "postgres",
                        password = "denji",
                        port = "5432")
            
            # creating a Cusor object to help execute queries "Insert requested info from customers"
            cursor = conn.cursor()
        
            # Since id are auto generated, search for the customer id based on their last name and return it   
            cursor.execute("SELECT customer_id FROM customer WHERE Last_name = %s;", (name,))
            ID = cursor.fetchone()[0]
            
            try: 
                cursor.execute("INSERT INTO Bikereturns VALUES (%s, %s, %s, %s, %s, %s)", (ID, rentalTime, now, rentalPeriod, bill, bike_Condition))
            except:
                raise
                print("Some Wrong value has been Input")
            else:
                #make changes to the database persistent
                conn.commit()
                
            print("Thanks for returning your bike. Hope you enjoyed our services!")
            print(f"That would be ${bill}")
            return bill
        
        else:
            print("Are you sure you rented a bike with us? If so enter the correct rentalPeriod and basis and numberOfBikes")
            return None
    
class customer(BikeRental, customer_info):
    """ remember to add some doc here
        """
    def __init__(self):
        #Add a custom exception to prevent any usage of this or any class before customer info is entered, Only allows for bike retrun
        
        """
        Our constructor method which instantiates various customer objects.
        """

        #customer_info().__init__(self)
        
        self._bikes = 0
        self._rentalBasis = 0
        self._bill = 0
        self._rentalTime = 0
        
    def requestBike(self):
        """
        Takes a request from the customer for the number of bikes.
        """
        name = input("Enter Last_name only again \n")
        bike_Condition = input("What is(are) the condition(s) of the bikes? \n")
    
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
                    self._rentalTime = BikeRental()._rentBikeOnHourlyBasis(self._bikes)
                    self._rentalBasis = 1
                    
                case 2:
                    self._rentalTime = BikeRental()._rentBikeOnDailyBasis(self._bikes)
                    self._rentalBasis = 2
                    
                case 3:
                    self._rentalTime = BikeRental()._rentBikeOnWeeklyBasis(self._bikes)
                    self._rentalBasis = 3
                    

            # Creating a connection object
            conn = psycopg2.connect(database = "BikeRentalsDatabase",
                        host = "127.0.0.1",
                        user = "postgres",
                        password = "denji",
                        port = "5432")
            
            # creating a Cusor object to help execute queries "Insert requested info from customers"
            cursor = conn.cursor()
        
            # Since id are auto generated, search for the customer id based on their last name and return it   
            cursor.execute("SELECT customer_id FROM customer WHERE Last_name = %s;", (name,))
            ID = cursor.fetchone()[0]
            
            try: 
                cursor.execute("INSERT INTO Rentals VALUES (%s, %s, %s, %s, %s)", (ID, self._bikes, self._rentalBasis, self._rentalTime, bike_Condition))
            except:
                print("Some Wrong value has been Input")
            else:
                #make changes to the database persistent
                conn.commit()
            
    def returnBike(self):
        """
        Allows customers to return their bikes to rental shop.
        """
  #--->> !! THis method should be independent of rentBike method
        
        if self._rentalBasis and self._rentalTime and self._bikes:
            BikeRental().returnBike((self._rentalTime, self._rentalBasis, self._bikes))
            #return (self._rentalTime, self._rentalBasis, self._bikes)
        else:
            #Id = int(input("Input Customer's ID"))
            #Search for the customers id in rental information if none ...
            return self._rentalTime, self._rentalBasis, self._bikes


