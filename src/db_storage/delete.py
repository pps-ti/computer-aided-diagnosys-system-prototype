from flask import Flask, session
from conn import db, storage

app = Flask(__name__)
app.secret_key = "rahasia"

def delete_hospital_account(id_user):
  db.child('akun_rs/' + id_user).remove()
  try :
    for file in [file.name for file in storage.list_files() if id_user in file.name]: storage.delete(file)
  except : pass

  return True

def delete_session():
  try: session.pop('admin')
  except: session.pop('user')
  return True

def delete_patient_data(id, disease, id_patient):
  db.child('akun_rs/' + id + '/patients_data/' + disease + '/' + id_patient).remove()
  storage.delete([data.name for data in storage.list_files() if id + '/' + disease + '/' + id_patient in data.name][0])
  return True