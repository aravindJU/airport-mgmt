import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
DATABASE = "airport.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/airline', methods=['GET', 'POST'])
def airline():
    conn = get_db_connection()
    if request.method == 'POST':
        if 'add' in request.form:
            conn.execute(
                'INSERT INTO Airline (AirlineID, AirlineCode, AirlineName, Country, Operation, ContactNo, Email) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (
                    request.form['AirlineID'],
                    request.form['AirlineCode'],
                    request.form['AirlineName'],
                    request.form['Country'],
                    request.form['Operation'],
                    request.form['ContactNo'],
                    request.form['Email']
                )
            )
            conn.commit()
        elif 'delete' in request.form:
            conn.execute('DELETE FROM Airline WHERE AirlineID = (SELECT MAX(AirlineID) FROM Airline)')
            conn.commit()
    airlines = conn.execute('SELECT * FROM Airline').fetchall()
    conn.close()
    return render_template('airline.html', airlines=airlines)

@app.route('/flights', methods=['GET', 'POST'])
def flights():
    conn = get_db_connection()
    if request.method == 'POST':
        if 'add' in request.form:
            conn.execute(
                'INSERT INTO Flights (FlightID, AirlineID, Airline, FlightNo, Departure, Arrival, DeptTime, ArrTime, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    request.form['FlightID'],
                    request.form['AirlineID'],
                    request.form['Airline'],
                    request.form['FlightNo'],
                    request.form['Departure'],
                    request.form['Arrival'],
                    request.form['DeptTime'],
                    request.form['ArrTime'],
                    request.form['Status']
                )
            )
            conn.commit()
        elif 'delete' in request.form:
            conn.execute('DELETE FROM Flights WHERE FlightID = (SELECT MAX(FlightID) FROM Flights)')
            conn.commit()
    flights = conn.execute('SELECT * FROM Flights').fetchall()
    conn.close()
    return render_template('flights.html', flights=flights)

@app.route('/passengers', methods=['GET', 'POST'])
def passengers():
    conn = get_db_connection()
    if request.method == 'POST':
        if 'add' in request.form:
            conn.execute(
                'INSERT INTO Passengers (PassengerID, FirstName, LastName, DOB, Gender, ContactNo, Email, FlightNo, Destination) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    request.form['PassengerID'],
                    request.form['FirstName'],
                    request.form['LastName'],
                    request.form['DOB'],
                    request.form['Gender'],
                    request.form['ContactNo'],
                    request.form['Email'],
                    request.form['FlightNo'],
                    request.form['Destination']
                )
            )
            conn.commit()
        elif 'delete' in request.form:
            conn.execute('DELETE FROM Passengers WHERE PassengerID = (SELECT MAX(PassengerID) FROM Passengers)')
            conn.commit()
    passengers = conn.execute('SELECT * FROM Passengers').fetchall()
    conn.close()
    return render_template('passengers.html', passengers=passengers)

@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    conn = get_db_connection()
    if request.method == 'POST':
        if 'add' in request.form:
            conn.execute(
                'INSERT INTO Bookings (BookingID, PassengerID, FlightID, SeatNo, BookingDate, PaymentStatus) VALUES (?, ?, ?, ?, ?, ?)',
                (
                    request.form['BookingID'],
                    request.form['PassengerID'],
                    request.form['FlightID'],
                    request.form['SeatNo'],
                    request.form['BookingDate'],
                    request.form['PaymentStatus']
                )
            )
            conn.commit()
        elif 'delete' in request.form:
            conn.execute('DELETE FROM Bookings WHERE BookingID = (SELECT MAX(BookingID) FROM Bookings)')
            conn.commit()
    bookings = conn.execute('SELECT * FROM Bookings').fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

@app.route('/staff', methods=['GET', 'POST'])
def staff():
    conn = get_db_connection()
    if request.method == 'POST':
        if 'add' in request.form:
            conn.execute(
                'INSERT INTO Staff (StaffID, FirstName, LastName, Role, ContactNo, Email, AirlineID) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (
                    request.form['StaffID'],
                    request.form['FirstName'],
                    request.form['LastName'],
                    request.form['Role'],
                    request.form['ContactNo'],
                    request.form['Email'],
                    request.form['AirlineID']
                )
            )
            conn.commit()
        elif 'delete' in request.form:
            conn.execute('DELETE FROM Staff WHERE StaffID = (SELECT MAX(StaffID) FROM Staff)')
            conn.commit()
    staff = conn.execute('SELECT * FROM Staff').fetchall()
    conn.close()
    return render_template('staff.html', staff=staff)

if __name__ == '__main__':
    app.run(debug=True)