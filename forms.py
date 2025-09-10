from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields import DateTimeField  # <-- Add this
from wtforms.validators import DataRequired, Email

# -------------------- AIRLINE FORM --------------------
class AirlineForm(FlaskForm):
    AirlineID = StringField('Airline ID', validators=[DataRequired()])
    AirlineCode = StringField('Airline Code', validators=[DataRequired()])
    AirlineName = StringField('Airline Name', validators=[DataRequired()])
    Country = StringField('Country', validators=[DataRequired()])
    Operation = StringField('Operation', validators=[DataRequired()])
    ContactNo = StringField('Contact No', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

# -------------------- FLIGHT FORM --------------------
class FlightForm(FlaskForm):
    AirlineID = SelectField('Airline', coerce=int, validators=[DataRequired()])
    FlightNo = StringField('Flight Number', validators=[DataRequired()])
    Departure = StringField('Departure', validators=[DataRequired()])
    Arrival = StringField('Arrival', validators=[DataRequired()])
    DeptTime = DateTimeField('Departure Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    ArrTime = DateTimeField('Arrival Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    Status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Add Flight')



# -------------------- PASSENGER FORM --------------------
class PassengerForm(FlaskForm):
    FirstName = StringField('First Name', validators=[DataRequired()])
    LastName = StringField('Last Name', validators=[DataRequired()])
    DOB = StringField('Date of Birth', validators=[DataRequired()])
    Gender = StringField('Gender', validators=[DataRequired()])
    ContactNo = StringField('Contact Number', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    FlightID = SelectField('Flight', coerce=int, validators=[DataRequired()])
    Destination = StringField('Destination', validators=[DataRequired()])
    submit = SubmitField('Add Passenger')


# -------------------- BOOKING FORM --------------------
class BookingForm(FlaskForm):
    PassengerID = SelectField('Passenger', coerce=int, validators=[DataRequired()])
    FlightID = SelectField('Flight', coerce=int, validators=[DataRequired()])
    SeatNo = StringField('Seat Number', validators=[DataRequired()])
    BookingDate = StringField('Booking Date', validators=[DataRequired()])
    PaymentStatus = StringField('Payment Status', validators=[DataRequired()])
    submit = SubmitField('Add Booking')


# -------------------- STAFF FORM --------------------
class StaffForm(FlaskForm):
    FirstName = StringField('First Name', validators=[DataRequired()])
    LastName = StringField('Last Name', validators=[DataRequired()])
    Role = StringField('Role', validators=[DataRequired()])
    ContactNo = StringField('Contact Number', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    AirlineID = SelectField('Airline', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Staff')
