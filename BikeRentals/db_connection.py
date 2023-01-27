# Inorder to connect to a PostgreSQL database instance use the psycopg2 library
import psycopg2
from BikeRentals.constants import database_info

# Use a context manager to help with clean up actions on the database
class Connect():
    def __enter__(self):
        """Connect to the postgreSQL server and link with the bike_rentals_db database

        Returns:
            connection object: alows to perform actions to the bike_rentals databse
        """
        try:
            self.connection = psycopg2.connect(**database_info) 
            print("Connection succesfull!")
            return self.connection
        
        except: # Catch all exceptions
            print("Could not connect to Database! An invalid argument maybe placed!")
            
    def __exit__(self):
            self.connection.close()
            self.connection = None
            
    
if __name__ == "__main__":
    with Connect() as conn:
        print("Succesful!!")