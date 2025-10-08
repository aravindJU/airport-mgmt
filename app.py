import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = "airport.db"

# -------------------- DB INITIALIZATION --------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL,
        Role TEXT NOT NULL
    )
    """)

    # Airline table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Airline (
        AirlineID INTEGER PRIMARY KEY,
        AirlineCode TEXT,
        AirlineName TEXT,
        Country TEXT,
        Operation TEXT,
        ContactNo TEXT,
        Email TEXT
    )
    """)

    # Flights table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Flights (
        FlightID INTEGER PRIMARY KEY,
        AirlineID INTEGER,
        Airline TEXT,
        FlightNo TEXT,
        Departure TEXT,
        Arrival TEXT,
        DeptTime TEXT,
        ArrTime TEXT,
        Status TEXT
    )
    """)

    # Passengers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passengers (
        PassengerID INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        DOB TEXT,
        Gender TEXT,
        ContactNo TEXT,
        Email TEXT,
        FlightNo TEXT,
        Destination TEXT
    )
    """)

    # Bookings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Bookings (
        BookingID INTEGER PRIMARY KEY,
        PassengerID INTEGER,
        FlightID INTEGER,
        SeatNo TEXT,
        BookingDate TEXT,
        PaymentStatus TEXT
    )
    """)

    # Staff table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Staff (
        StaffID INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        Role TEXT,
        ContactNo TEXT,
        Email TEXT,
        AirlineID INTEGER
    )
    """)

    # Insert admin user if not exists
    cursor.execute("""
    INSERT OR IGNORE INTO Users (Username, Password, Role)
    VALUES ('admin', '1234', 'admin')
    """)

    conn.commit()
    conn.close()

# Initialize DB on every app start
init_db()

# -------------------- DB CONNECTION --------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------- LOGIN REQUIRED DECORATOR --------------------
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Please login first!', 'warning')
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash('Access denied!', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# -------------------- HOME --------------------
@app.route('/')
def home():
    return render_template('home.html')

# -------------------- REGISTER --------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = 'user'  # normal users
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO Users (Username, Password, Role) VALUES (?, ?, ?)',
                         (username, password, role))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

# -------------------- LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE Username = ?', (username,)).fetchone()
        conn.close()
        if user:
            # Admin login
            if user['Username'] == 'admin' and password == 'xAgRK342':
                session['user_id'] = user['UserID']
                session['username'] = user['Username']
                session['role'] = 'admin'
                flash('Admin login successful!', 'success')
                return redirect(url_for('home'))
            # Normal user login
            elif check_password_hash(user['Password'], password):
                session['user_id'] = user['UserID']
                session['username'] = user['Username']
                session['role'] = user['Role']
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))

# -------------------- CHANGE PASSWORD --------------------
@app.route('/change_password', methods=['GET', 'POST'])
@login_required()
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash("New password and confirmation do not match.", "danger")
            return redirect(url_for('change_password'))

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE UserID = ?', (session['user_id'],)).fetchone()

        # Check old password
        if not check_password_hash(user['Password'], old_password):
            flash("Old password is incorrect.", "danger")
            conn.close()
            return redirect(url_for('change_password'))

        # Update password (always hashed)
        conn.execute('UPDATE Users SET Password = ? WHERE UserID = ?',
                     (generate_password_hash(new_password), session['user_id']))
        conn.commit()
        conn.close()
        flash("Password changed successfully!", "success")
        return redirect(url_for('home'))

    return render_template('change_password.html')


# -------------------- ADMIN ONLY TABLES --------------------
@app.route('/airline', methods=['GET', 'POST'])
@login_required(role='admin')
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
@login_required(role='admin')
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

@app.route('/staff', methods=['GET', 'POST'])
@login_required(role='admin')
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

# -------------------- PASSENGERS & BOOKINGS (ALL USERS) --------------------
@app.route('/passengers', methods=['GET', 'POST'])
@login_required()
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
@login_required()
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

# -------------------- RUN APP --------------------
if __name__ == '__main__':
    app.run(debug=True)
