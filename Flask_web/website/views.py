from calendar import Calendar
from datetime import date
from flask import Blueprint, abort, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from wtforms import DateTimeField, IntegerField, SelectField, StringField, SubmitField
from .models import AppointmentForm, Note,User,Patient,Appointment
from flask_wtf import FlaskForm
from wtforms_alchemy import QuerySelectField

from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
   
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# todo kalendarz z wizytami all
@views.route('/calendar')
def calendar():
   
    return render_template('calendar.html',user=current_user)

@views.route('/patient')
def patient():
    patients = Patient.query.all()
    return render_template('patient.html', patients=patients,user=current_user)


@views.route('/addPatient', methods=['GET','POST'])
def addpatient():
    if request.method == 'POST':
        
        name = request.form.get('name')
        sur_name = request.form.get('sur_name')
        numer = request.form.get('numer')
        notka = request.form.get('notka')
        new_patient = Patient(name=name, sur_name=sur_name, numer=numer,notka=notka,user_id=current_user.id)
        db.session.add(new_patient)
        db.session.commit()
            
        flash('Pacjent dodany!', category='success')
        return redirect('/patient')
    return render_template('addPatient.html', user=current_user)

@views.route('/deletePatient/<int:id>')
def deletePatient(id):
    patient_to_delete= Patient.query.get_or_404(id)
    db.session.delete(patient_to_delete)
    db.session.commit()

    flash('Pacjent usunięty')
    return redirect(url_for('views.patient',user=current_user))


class PatientForm(FlaskForm):
    name = StringField("name")
    sur_name =StringField("sur_name")
    numer = IntegerField("numer")
    notka=StringField("notka")



@views.route('/editPatient/<int:id>', methods=['GET','POST'])
def editPatient(id):
    form=PatientForm()
    patient_to_edit= Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient_to_edit.name=request.form['name']
        patient_to_edit.sur_name=request.form['sur_name']
        patient_to_edit.numer=request.form['numer']
        patient_to_edit.notka=request.form['notka']
        
        db.session.commit()

        flash('Edycja zapisana')
        return redirect('/patient')
    return render_template('updatePatient.html', user=current_user, form=form, patient_to_edit=patient_to_edit)



def chosePatient():      
    return db.session.query(patient).all()


@views.route('/appointment', methods=['GET','POST'])
def appointment():
    appointments = Appointment.query.all()
    form = AppointmentForm()
    form.patient_id.query=Patient.query.all()

    return render_template('appointment.html',user=current_user,form=form)



    