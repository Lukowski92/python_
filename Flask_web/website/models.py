import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from wtforms import DateField, DateTimeField, IntegerField, StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms_alchemy import QuerySelectField
from wtforms.validators import DataRequired


# todo zmienić na kartępacjenta pacjent i jego wszyskite wizyty i notataki ?
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    patients = db.relationship('Patient')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sur_name = db.Column(db.String(100), nullable=False)
    numer = db.Column(db.Integer, unique=True)
    notka=db.Column(db.String(10000), nullable=False)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    note_at_regis = db.Column(db.String(1000))
    note_at = db.Column(db.String(1000))
    note_after = db.Column(db.String(1000))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    
    



