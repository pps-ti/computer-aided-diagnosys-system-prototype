from conn import db
from flask import request, redirect

# CHANGE THE ADMIN PASSWORD
def change_admin_pwd(id):
  db.child('akun_admin/'+id+'/sandi').set(request.form['pwd1'])
  return True

# ADMIN CHANGE HOSPITAL ACCOUNT
def change_hospital_account(id, id_user):
  db.child('akun_rs/' + id_user).update({
    "address" : request.form['address'],
    "email" : request.form['email'],
    "hospital_name" : request.form['hospital_name'],
    "province" : request.form['province'],
    "pwd" : request.form['pwd']
  })

  if db.child('akun_rs/'+id_user).get().val()['verified'] == 'Y':
    return redirect('/admin/'+id+'/registered_accounts')
  else:
   return redirect('/admin/'+id+'/queue')

# USER CHANGE THEIR DATA
def change_user_data(id):
  db.child('akun_rs/'+id).update({
    "address" : request.form['hospital_address'],
    "email" : request.form['email'],
    "hospital_name" : request.form['hospital_name'],
    "province" : request.form['province'],
  })

  db.child('akun_rs/'+id).update({ "pwd" : request.form['new_pwd2'] }) if request.form['new_pwd2'] != '' else db.child('akun_rs/'+id).update({ "pwd" : request.form['old_pwd'] })
    
  return redirect('/')

# USER CHANGE PATIENT DATA
def change_patient_data(id, disease, id_patient):
  from flask import url_for

  db.child('akun_rs/' + id + '/patients_data/' + disease + '/' + id_patient).update({
      "address" : request.form['address'],
      "birth_date" : request.form['birth_date'],
      "blood_type" : request.form['blood_type'],
      "email" : request.form['email'],
      "gender" : request.form['gender'],
      "height" : request.form['height'],
      "name" : request.form['name'],
      "result" : request.form['result'],
      "weight" : request.form['weight']
    })
  
  return redirect(url_for('diagnosed', id = id, disease = disease))

# GENERATE UNIQUE CODE FOR NEW PASSWORD
def get_new_password():
  from random import choice
  from flask import render_template
  from string import ascii_uppercase, digits
  
  import sys, os
  sys.path.append(os.path.abspath(os.path.join('..', 'src')))
  from src.mail_services import send_email

  # it will generate the unique code in order to gain the new password
  for i in db.child('akun_rs').get().val():
    if db.child('akun_rs/' + i).get().val()['email'] == request.form['email']:
      unique_code_pwd = ''.join(choice(ascii_uppercase + digits) for _ in range(20))
      db.child('akun_rs/' + i + '/frgt_pwd_code').set(unique_code_pwd)
      break

  # send the unique code to your email
  try:
    if send_email('Request access to login', tambahan = unique_code_pwd): return render_template("auth/unique_code_sent.html")

  # if email (the account) isn't not exist in database
  except: return render_template("auth/forgot-password.html", msg = "Your account is not found!\nMake sure that email you've entered is correct.")

# SET NEW PASSWORD THROUGH THE NEW UNIQUE CODE
def change_user_pwd():
  from flask import render_template
  # it will reset your old password with the new one
  for i in db.child('akun_rs').get().val():
    if db.child('akun_rs/'+i).get().val()['email'] == request.form['email'] and db.child('akun_rs/'+i).get().val()['frgt_pwd_code'] == request.form['unique_code']:
      db.child('akun_rs/'+i+'/frgt_pwd_code').remove()
      db.child('akun_rs/'+i+'/pwd').set(request.form['pwd2'])
      success = True
    
  try:
    if success: return render_template("auth/new_pwd_success.html")
  except: return render_template("auth/new_pwd.html", msg = "Incorrect Email/unique code!")