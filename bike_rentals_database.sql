/* Customer table that stores customer's personal information */

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


-- Create Rentals table

/* Rentals table contains both pending and returned bikes from customer */

CREATE TABLE Rentals (
	customer_id INT NOT NULL,
	no_of_bikes INT NOT NULL,
	rentalBasis INT NOT NULL CHECK (rentalBasis =1 AND rentalBasis=2 AND rentalBasis=3),
	timeRented TIMESTAMP NOT NULL,
	bikeCondition VARCHAR(10),
	FOREIGN KEY (customer_id) REFERENCES Customer (customer_id) --set customer_id as foreign key
	);





