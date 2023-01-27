/* Customer table that stores customer's personal information */

-- Table structure for table 'category'

CREATE TABLE Customer (
	customer_id SERIAL PRIMARY KEY, --autogenerate customer id
	First_name VARCHAR(30) NOT NULL,
	Last_name VARCHAR(30) NOT NULL,
	Age INT NOT NULL,
	Gender VARCHAR(20) DEFAULT 'Prefer not to say',
	Phone_no INT NOT NULL,
	email VARCHAR(100),
	Location VARCHAR(50) NOT NULL
);

/* Add a check constraint to to age column */
ALTER TABLE Customer 
ADD CONSTRAINT Age CHECK (age >= 18);

/* add a unique constraint to the phone_no column */
ALTER TABLE Customer
ADD CONSTRAINT Phone_no UNIQUE (Phone_no);

-- -------------------------------------------------------------------

-- Table structure for table 'Rentals'

/* Rentals table contains both pending and returned bikes from customer.
	All columns to cantain NOT NULL constraint*/

CREATE TABLE Rentals (
	customer_id INT NOT NULL,
	no_of_bikes INT NOT NULL,
	rentalBasis INT NOT NULL CHECK (rentalBasis =1 AND rentalBasis=2 AND rentalBasis=3), -- 3 kinds of rental basis only
	timeRented TIMESTAMP NOT NULL,
	bikeCondition VARCHAR(10),
	FOREIGN KEY (customer_id) REFERENCES Customer (customer_id) --set customer_id as foreign key
	);

-- Update the foreing key "ON DELETE CASCADE"
ALTER TABLE Rentals ADD CONSTRAINT customer_id
FOREIGN KEY (customer_id) REFERENCES Customer ON DELETE CASCADE;

-- ----------------------------------------------------------------------

-- Table structure for table 'bikeReturns'

/* The bikeReturns table to only contain the records of customers that have returned bikes.
	.... */
	
CREATE TABLE bikeReturns (
	customer_id INT NOT NULL,
	timeRented TIMESTAMP NOT NULL,
	timeReturned TIMESTAMP NOT NULL,
	Total_time_taken TEXT NOT NULL,
	Bill REAL NOT NULL,
	Bike_condition VARCHAR(10) NOT NULL
	);
	
-- -------------------------------------------------------

/* Test the correctness of the customer table created by adding some data to it
*  Damping data for table 'customer'
*/
INSERT INTO customer (First_name, Last_name, Age, Gender, Phone_no, email, Location) 
VALUES 
	('lENOX', 'MIHESO', 20, 'Male', 254701234567, 'lenox@xyz.com', 'Djibouti'),
	('Pete', 'Davidson', 40, 'Male', 01234567890, 'pete@xyz.com', 'Mali');

/* Since phone number INT type size is less, Update the datatype to bigint for larger storage size
to overcome the error integer out of range since phone number takes more than 4 byte storage size */
ALTER TABLE customer ALTER COLUMN
Phone_no TYPE BIGINT;


--view the data available in the customer table
SELECT * FROM CUSTOMER;

-- First_name Lenox has incorrect case; update
UPDATE customer
	SET first_name = 'LENOX'
	WHERE customer_id = 1 ;
	
/* Test the correctness of the Rentals table created by adding some data to it
* ...
*
*/
INSERT INTO Rentals
VALUES 
	(1, 5, 1, '2022-12-30 08:30:22', 'Good' );

/* update the check constraint in rentals table to do away with this error;
	new row for relation "rentals" violates check constraint "rentals_rentalbasis_check" */
	
ALTER TABLE Rentals ADD CONSTRAINT rentalBasis CHECK (rentalBasis =1 OR rentalBasis=2 OR rentalBasis=3);

SELECT * FROM Rentals;

/* Test the correctness of the bikeReturns table created by adding some data to it
* ...
*/

INSERT INTO bikeReturns
VALUES 
	(1, '2022-12-30 08:30:22', '2022-12-30 011:30:22', '5', 25.012, 'Good' );
	
SELECT * FROM bikeReturns;