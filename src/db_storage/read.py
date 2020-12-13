import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from conn import db

def get_id(email, password, akun_rs = True, regis = "N"):
  # TO CHECKING THE USER ID IN DATABASE
  if regis != "N" and akun_rs:
    for i in db.child('akun_rs').get().val():
      if db.child('akun_rs/'+i).get().val()['email'] == email and db.child('akun_rs/'+i).get().val()['hospital_name'] == regis[0] and db.child('akun_rs/'+i).get().val()['address'] == regis[1] : return i
  
  # USER ID
  elif akun_rs:
    for i in db.child('akun_rs').get().val():
      if db.child('akun_rs/'+i).get().val()['email'] == email and db.child('akun_rs/'+i).get().val()['pwd'] == password : return i
  
  # ADMIN ID
  elif akun_rs == False:
    for i in db.child('akun_admin').get().val():
      if db.child('akun_admin/'+i).get().val()['email'] == email and db.child('akun_admin/'+i).get().val()['sandi'] == password : return i

# FOR LANDING PAGE
def check_session():
  from flask import session, redirect, url_for, Flask
  
  app = Flask(__name__)
  app.secret_key = "rahasia"

  try :
    if session['admin'] != None : return redirect(url_for('dashboard_admin', id = session['admin']))
  except:
    if session['user'] != None : return redirect(url_for('dashboard_user', id = session['user']))

def user_login():
  from flask import request, redirect, url_for, render_template, session, Flask

  if request.method =='POST':
    app = Flask(__name__)
    app.secret_key = "rahasia"
  
    # login as administrator
    if get_id(request.form['email'], request.form['sandi'], akun_rs=False) != None:
      session['admin'] = get_id(request.form['email'], request.form['sandi'], akun_rs=False)
      return redirect(url_for('dashboard_admin', id = session['admin']))
      
    # login as user
    elif get_id(request.form['email'], request.form['sandi']) != None:
      session['user'] = get_id(request.form['email'], request.form['sandi'])
      return redirect(url_for('dashboard_user', id = session['user']))
      
    # error handler
    else:
      return render_template("auth/login.html", pesan = "Incorrect email/password!")
  else:
    return render_template("auth/login.html")

# GET USER/ADMIN ACOUNT ID
def get_id_account(id, sandi = None):
  if sandi == None: return [id, db.child('akun_rs/'+id).get().val()]
  else: return [id, db.child('akun_admin/'+id).get().val()['sandi']]

# GET DIAGNOSED PATIENTS DATA:
def get_patients_data(id, disease):
  return dict(db.child('akun_rs/' + id + '/patients_data/' + disease).get().val().items())

# GET USERS DATA :
def data_users(verified = 'Y'):
  data = {}
  
  if verified == 'Y':
    for i in db.child('akun_rs/').get().val():
      if db.child('akun_rs/').get().val()[i]['verified'] == 'Y': data[i] = dict(db.child('akun_rs/' + i).get().val().items())
  else:
    for i in db.child('akun_rs/').get().val():
      if db.child('akun_rs/').get().val()[i]['verified'] != 'Y': data[i] = dict(db.child('akun_rs/' + i).get().val().items())

  return data

# REDIRECTING USERS TO DASHBOARD
def user_dashboard(id):
  from flask import render_template, request
  from conn import storage

  if db.child("akun_rs/" + id).get().val()['verified'] == "Y": return render_template('users/dashboard.html', id = get_id_account(id))
    
  else:
    if request.method == 'POST':
      if request.form['unique_code'] == db.child("akun_rs/" + id).get().val()['verified']:
        storage.child(id + "/0.txt").put(os.path.join(os.path.dirname(os.path.abspath(__file__)), '0.txt'))
        db.child("akun_rs/" + id).update({"verified" : "Y" })
        return render_template('users/dashboard.html',id = get_id_account(id), pesan = "Your account has been activated successfully!")
        
      else: return render_template('users/verification.html', id = id, pesan = "The unique code is not correct!")
      
    return render_template('users/verification.html', id = id)