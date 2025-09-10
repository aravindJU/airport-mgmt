import sqlite3

conn = sqlite3.connect('airport.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS Airline(
    AirlineID INTEGER PRIMARY KEY,
    AirlineCode CHAR(2),
    AirlineName VARCHAR(30),
    Country VARCHAR(30),
    Operation VARCHAR(30),
    ContactNo CHAR(10),
    Email VARCHAR(30)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Flights(
    FlightID INTEGER PRIMARY KEY,
    AirlineID INTEGER,
    Airline VARCHAR(30),
    FlightNo INTEGER,
    Departure VARCHAR(30),
    Arrival VARCHAR(30),
    DeptTime TIME,
    ArrTime TIME,
    Status VARCHAR(10),
    FOREIGN KEY (AirlineID) REFERENCES Airline(AirlineID)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Passengers( 
    PassengerID INTEGER PRIMARY KEY, 
    FirstName VARCHAR(30), 
    LastName VARCHAR(30), 
    DOB DATE, 
    Gender CHAR(1), 
    ContactNo CHAR(10), 
    Email VARCHAR(30), 
    FlightNo INTEGER, 
    Destination VARCHAR(30)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Bookings(
    BookingID INTEGER PRIMARY KEY,
    PassengerID INTEGER,
    FlightID INTEGER,
    SeatNo INTEGER,
    BookingDate DATE,
    PaymentStatus VARCHAR(30),
    FOREIGN KEY (PassengerID) REFERENCES Passengers(PassengerID),
    FOREIGN KEY (FlightID) REFERENCES Flights(FlightID)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Staff(
    StaffID INTEGER PRIMARY KEY,
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    Role VARCHAR(10),
    ContactNo CHAR(10),
    Email VARCHAR(30),
    AirlineID INTEGER,
    FOREIGN KEY (AirlineID) REFERENCES Airline(AirlineID)
)
''')

conn.commit()
conn.close()