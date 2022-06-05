import datetime

from sqlalchemy import true
from cardiology import patient
from cardiology.models import Appointments, Patients
import os
import secrets
import re


def parse_time(day, time):
    d = day.split('-')
    t = time.split(':')
    x = datetime.date(int(d[0]), int(d[1]), int(d[2]))
    y = datetime.time(int(t[0]), int(t[1]))
    return x, y


def generate_gcalendar_link(title: str, description: str, start: datetime, end: datetime):
    return f'https://www.google.com/calendar/render?action=TEMPLATE&text={title}&details={description}&dates={re.sub("[-:]", "", start.isoformat()).split(".", 1)[0]}/{re.sub("[-:]", "", end.isoformat()).split(".", 1)[0]}'


def availabe_appointments(doc, day):
    all_appointmnts = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30']
    reserved_appointments = Appointments.query.filter_by(d_id=doc.d_id, date=day).all()
    reserved_times = [i.Time.strftime('%H:%M') for i in reserved_appointments]
    availabe_time = list(set(all_appointmnts) - set(reserved_times))

    return sorted(availabe_time)


def save_picture(form_picture, folder_name):
    fname = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = fname + f_ext
    basepath = os.path.dirname(__file__)
    picture_path = os.path.join(f'{basepath}/static/{folder_name}', picture_fn)
    form_picture.save(picture_path)
    saving_path = f'../static/{folder_name}/{picture_fn}'
    return saving_path

def sorting_appointments(appointments, type):
    appoints = [x for x in appointments if x.date>=datetime.date.today()]
    appoints = sorted(appointments, key= lambda x:x.date and x.Time)
    if type=='patient':
        if len(appoints)>=3:
            return appoints[0:3]
        else:
            return appoints[0:len(appoints)]
    return appoints


def doct_patient(appointments):
    patients=[]
    for i in appointments:
        p= Patients.query.filter_by(p_id=i.p_id).first()
        patients.append(p)
    patients = list(set(patients))
    return patients




    