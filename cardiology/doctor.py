from flask import render_template, redirect, url_for, Flask, request, flash
from flask_sqlalchemy import SQLAlchemy
from cardiology.models import Doctors, Patients, Admins, Appointments, Medical_records, p_Messages, Scans, Prescription
from cardiology import app, db
from datetime import datetime, date
from cardiology.my_functions import  save_picture, doct_patient
from flask_login import current_user, login_required

#-------------------------------------
d_user = Doctors.query.filter_by(d_id=1).first()
selected_patient = Patients.query.filter_by(p_id=3).first()

#-------------------------------------
@app.route('/DoctorProfile', methods=['GET', 'POST'])
def doc_profile():
    global selected_patient
    doc_appoints = Appointments.query.filter_by(d_id=d_user.d_id).all()
    doc_patients = doct_patient(doc_appoints)
    doc_msgs= p_Messages.query.filter_by(d_id=d_user.d_id).all()
    if request.method == 'POST':
        patient_id = request.form['p_id']
        selected_patient = Patients.query.filter_by(p_id=patient_id).first()
        redirect(url_for('patientinfo'))


    return render_template('Doctor.html', user=d_user, patients=doc_patients, msgs=doc_msgs)

@app.route('/PatientInfo')
def patient_info():

    MR = Medical_records.query.filter_by(p_id=selected_patient.p_id).first()
    PRs = Medical_records.query.filter_by(p_id=selected_patient.p_id).all()
    appoints = Appointments.query.filter_by(p_id=selected_patient.p_id).all()
    PRs.reverse()
    return render_template('Doctor_Patients.html', user=d_user, patient=selected_patient, MR=MR, PRs=PRs, appoints=appoints)

@app.route('/AddMedicalRecord', methods=['GET', 'POST'])
def add_MR():

    if request.method == 'POST':
        if Medical_records.query.filter_by(p_id=selected_patient.p_id).all()==[]:
            new_MR = Medical_records(p_id=selected_patient.p_id, p_name=selected_patient.p_name, d_id=d_user.d_id,
            d_name=d_user.d_name, diseases_history=request.form['medical_history'],
            restricted_drugs=request.form['restricted_drugs'])
            db.session.add(new_MR)
        else:
            mr=Medical_records.query.filter_by(p_id=selected_patient.p_id).first()
            mr.restricted_drugs=request.form['restricted_drugs']
            mr.diseases_history=request.form['medical_history']
        db.session.commit()
        flash('Medical Record is edited successfully.')
        redirect(url_for('patient_info'))

    return render_template('.html', user=d_user)

@app.route('/AddPrescription', methods=['GET', 'POST'])
def add_PR():

    if request.method == 'POST':
        new_PR = Prescription(p_id=selected_patient.p_id, p_name=selected_patient.p_name, d_id=d_user.d_id,
            d_name=d_user.d_name, diagnosis=request.form['diagnosis'], drugs=request.form[''],
            pre_date=date.today())
        db.session.add(new_PR)
        db.session.commit()
        flash('Prescription is added successfully.')
        redirect(url_for('patient_info'))

    return render_template('.html', user=d_user)

@app.route('/DoctorAppointments')
def doctor_appoints():

    doc_appoints = Appointments.query.filter_by(d_id=d_user.d_id).all()

    return render_template('.html', user=d_user, apponts=doc_appoints)

@app.route('/EditDoctorInfo', methods=['GET', 'POST'])
def edit_doc():
    if request.method == 'POST':
        d_user.d_username = request.form['']
        d_user.d_email = request.form['']
        d_user.d_phone = request.form['']    
        d_user.passward = request.form['']    
        db.session.commit()
        flash('proile is updated successfully')

