from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Airline(db.Model):
    __tablename__ = 'Airline'
    AirlineID = db.Column(db.Integer, primary_key=True)
    AirlineCode = db.Column(db.String(2))
    AirlineName = db.Column(db.String(30))
    Country = db.Column(db.String(30))
    Operation = db.Column(db.String(30))
    ContactNo = db.Column(db.String(10))
    Email = db.Column(db.String(30))

class Flights(db.Model):
    __tablename__ = 'Flights'
    FlightID = db.Column(db.Integer, primary_key=True)
    AirlineID = db.Column(db.Integer, db.ForeignKey('Airline.AirlineID'))
    Airline = db.Column(db.String(30))
    FlightNo = db.Column(db.Integer)
    Departure = db.Column(db.String(30))
    Arrival = db.Column(db.String(30))
    DeptTime = db.Column(db.Time)
    ArrTime = db.Column(db.Time)
    Status = db.Column(db.String(10))

class Passengers(db.Model):
    __tablename__ = 'Passengers'
    PassengerID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(30))
    LastName = db.Column(db.String(30))
    DOB = db.Column(db.Date)
    Gender = db.Column(db.String(1))
    ContactNo = db.Column(db.String(10))
    Email = db.Column(db.String(30))
    FlightNo = db.Column(db.Integer)
    Destination = db.Column(db.String(30))

class Bookings(db.Model):
    __tablename__ = 'Bookings'
    BookingID = db.Column(db.Integer, primary_key=True)
    PassengerID = db.Column(db.Integer, db.ForeignKey('Passengers.PassengerID'))
    FlightID = db.Column(db.Integer, db.ForeignKey('Flights.FlightID'))
    SeatNo = db.Column(db.Integer)
    BookingDate = db.Column(db.Date)
    PaymentStatus = db.Column(db.String(30))

class Staff(db.Model):
    __tablename__ = 'Staff'
    StaffID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(30))
    LastName = db.Column(db.String(30))
    Role = db.Column(db.String(10))
    ContactNo = db.Column(db.String(10))
    Email = db.Column(db.String(30))
    AirlineID = db.Column(db.Integer, db.ForeignKey('Airline.AirlineID'))
