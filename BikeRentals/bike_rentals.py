import datetime
from BikeRentals.db_connection import Connect


class customer_info:
    def __init__(self, Fisrt_Name: str, Last_name: str, Age: int, Gender: str, Phone_no: int, email: str, Location: str):
        
        """
        Our constructor method which allows for saving of individual customer infomation to a csv file, "Bike_rental_Customer_info.csv"
        """
        
        #self.ID = ID
        self.First_name = Fisrt_Name
        self.Last_name = Last_name
        self.Gender = Gender
        self.Phone_no = Phone_no
        self.Age = Age
        self.email = email
        self.Location = Location

    # save customer information into database
    def commit_info(self):
        
        with Connect() as conn:
            self.cursor = conn.cursor()
            
            # Insert the customer details into the databse by passing the data to fill the placeholders
            try:
                self.cursor.execute("INSERT INTO customer (First_name, Last_name, Age, Gender, Phone_no, email, Location) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                (self.First_name, self.Last_name, self.Age, self.Gender, self.Phone_no, self.email, self.Location))
                print("Customer details has been setup. Proceed to rentals!")
            except:
                print("Some Wrong value has been Input")
                
        
class BikeRental():
    def set_stock(self, stock=0):
        """
        constructor class that instantiates bike rental shop.
        """
        self._stock = stock
        
    def displaystock(self):
        """
        Displays the number of bikes currently available for rent in the shop.
        """
        # print(f"We currently have {self._stock} bikes available to rent.")
        return self._stock
        
    def _rentBikeOnHourlyBasis(self, n):
        """
        Rent bike on hourly basis to a customer.
        """
        now = datetime.datetime.now()
        print(f"You have rented {n} bike(s) on hourly basis on {now.date()} at {now.time()} hours.")
        print("You will be charged $5 for each hour per bike.")
        print("We hope that you enjoy our service.")

        self._stock -= n
        return now
    
    def _rentBikeOnDailyBasis(self, n):
        """
        rent bike on daily basis to a customer.
        """
            
        now = datetime.datetime.now()
        print(f"You have rented {n} bike(s) on daily basis on {now.date()} at {now.time()} hours.")
        print("You will be charged $20 for each day per bike.")
        print("We hope that you enjoy our service.")
            
        self._stock -= n
        return now
            
    def _rentBikeOnWeeklyBasis(self, n):
        """
        Rent bike on hourly basis to a customer.
        """
            
        now = datetime.datetime.now()
        print(f"You have rented {n} bike(s) on weekly basis on {now.date()} at {now.time()} hours.")
        print("You will be charged $60 for each week per bike.")
        print("We hope that you enjoy our service.")
            
        self._stock -= n
        return now
        
    def returnBike(self, request):
        """
        1. Accept a rented bike from a customer.
        2. Replenishes the inventory.
        3. Return a bill
        Implement a default time period of an hour, Daily, weekly if the duration spent is
        less than an hour, day or week respectively.
        """
        
        # extract the tuple and initiate the bill
        rentalTime, rentalBasis, numOfBikes = request
        bill = 0
        
        # issue a bill only if all three parameters are not null!
        if rentalTime and rentalBasis and numOfBikes:
            self._stock += numOfBikes
            now = datetime.datetime.now()
            rentalPeriod = now - rentalTime
            
            # Note: The Match statements require Python 3.10 or newer
            match rentalBasis:
                # hourly bill calculation
                case 1:
                    if (rentalPeriod.total_seconds()/3600) < 1:
                        bill = 5
                    else:
                        bill = round(rentalPeriod.total_seconds()/3600) * 5 * numOfBikes
                        
                # daily bill calculation
                case 2:
                    if (rentalPeriod.days) == 0:
                        bill = 20
                    else:
                        bill = round(rentalPeriod.days) * 20 * numOfBikes
                        
                # weekly bill calculation
                case 3:
                    if (rentalPeriod.days/7) < 1:
                        bill = 60
                    else: 
                        bill = round(rentalPeriod.days /7) * 60 * numOfBikes
                    
            # family discount calculation
            if (3 <= numOfBikes <= 5):
                print("You are eligible for family rental promotion of 30% discount")
                bill = bill * 0.7

            
            name = input("Enter Last_name only again \n")
            bike_Condition = input("What is(are) the condition(s) of the bikes? \n")

            with Connect() as conn:
                # creating a Cusor object to help execute queries "Insert requested info from customers"
                cursor = conn.cursor()
            
                # Since id are auto generated, search for the customer id based on their last name and return it   
                cursor.execute("SELECT customer_id FROM customer WHERE Last_name = %s;", (name,))
                ID = cursor.fetchone()[0]
                
                # ---->> Rather than checking for the ID or name in DB just check from the instantiated class
                
                try: 
                    cursor.execute("INSERT INTO Bikereturns VALUES (%s, %s, %s, %s, %s, %s)", (ID, rentalTime, now, rentalPeriod, bill, bike_Condition))
                except:
                    raise
                else:
                    #make changes to the database persistent
                    conn.commit()
                
            print("Thanks for returning your bike. Hope you enjoyed our services!")
            print(f"Total bill is ${bill}")
            return bill
        
        else:
            print("Are you sure you rented a bike with us?")
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
            return None
        
        if self._bikes < 1:
            print("Invalid input. Number of bikes should be greater than zero!")
            return None

        elif self._bikes > self.displaystock():
            print(f"Sorry! We have currently {self.displaystock()} bikes available to rent.")
            return None
        
        else:
            self._rentalBasis = int(input("Enter your Rental Basis: "))
            
            match self._rentalBasis:
                case 1:
                    self._rentalTime = self._rentBikeOnHourlyBasis(self._bikes)
                    
                case 2:
                    self._rentalTime = self._rentBikeOnDailyBasis(self._bikes)
                    
                case 3:
                    self._rentalTime = self._rentBikeOnWeeklyBasis(self._bikes)
                    
        
            with Connect() as conn:
            
                # creating a Cusor object to help execute queries "Insert requested info from customers"
                cursor = conn.cursor()
            
                # Since id are auto generated, search for the customer id based on their last name and return it   
                cursor.execute("SELECT customer_id FROM customer WHERE Last_name = %s;", (name,))
                ID = cursor.fetchone()[0]
                if ID == None or '':
                    print("Your information does not exist in the database!")
                    return None
                
                try: 
                    cursor.execute("INSERT INTO Rentals VALUES (%s, %s, %s, %s, %s)", (ID, self._bikes, self._rentalBasis, self._rentalTime, bike_Condition))
                except:
                    print("Some Wrong value has been Input")
                else:
                    #make changes to the database persistent
                    conn.commit()
            
            return self._bikes
            
    def custReturnBike(self):
        """
        Allows customers to return their bikes to rental shop.
        """
  #--->> !! THis method should be independent of rentBike method
        
        if self._rentalBasis and self._rentalTime and self._bikes:
            self.returnBike((self._rentalTime, self._rentalBasis, self._bikes))
            
        else:
            self.returnBike((0, 0, 0))


