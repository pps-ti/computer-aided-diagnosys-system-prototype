from flask import Flask, request, render_template
from flask_mail import Mail, Message
import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from db_storage.conn import db

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rahasia'
app.config['MAIL_PASSWORD'] = 'rahasia'

mail = Mail(app)

def send_email(subjek, id = None, tambahan = None):
  if subjek == "Activation code":
    penerima = [request.form['email']]
    pesan = "This is the code to activate your account : \n" + tambahan + "\n\nInput the code above from your dashboard after login."
  
  elif subjek == "Activation Code":
    penerima = [db.child("akun_rs/" + id).get().val()['email']]
    pesan = "This is the code to activate your account : \n" + db.child("akun_rs/" + id).get().val()['verified'] + "\n\nInput the code above from your dashboard after login."

  elif subjek == "Request access to login":
    penerima = [request.form['email']]
    pesan = 'Please use this unique code below to get new password:\n' + tambahan + '\n\nThanks!'

  elif subjek == "User complaint":
    penerima = ['roploverz@gmail.com']
    pesan = 'Complaint from ' + db.child('akun_rs/' + id).get().val()['email'] + '\n'+ 'Message :\n' + request.form['message']

  msg = Message(subjek, sender = "noreply.neurahealth@gmail.com", recipients = penerima)
  msg.body = pesan
  mail.send(msg)
  
  return True

def send_diagnose_result(proba, image, hasil):
  msg = Message("Diagnose Result!", sender= 'noreply.neurahealth@gmail.com', recipients = [request.form['email']])
  msg.html = render_template('/users/diagnosed_email.html', image = image, proba = proba, hasil_diagnosa = hasil)
  mail.send(msg)
