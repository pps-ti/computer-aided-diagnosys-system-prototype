from conn import db, storage
from flask import request, render_template, redirect, url_for
from read import get_id
from random import choice
from string import ascii_uppercase, digits
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'src')))

# HELPER FUNCTION
def check_redundant():
  if get_id(request.form['email'], None, regis=[request.form['hospital_name'], request.form['hospital_address']]) not in [i for i in db.child('akun_rs').get().val()]:
    unique_code = ''.join(choice(ascii_uppercase + digits) for _ in range(6))

    db.child('akun_rs/' + unique_code ).set({
      "hospital_name" : request.form['hospital_name'],
      "email" : request.form['email'],
      "pwd" : request.form['pwd'],
      "address" : request.form['hospital_address'],
      "province" : request.form['province'],
      "verified" : unique_code,
      "patients_data" : "None"
    })

  else: unique_code = None

  return unique_code

# REGISTER NEW ACCOUNT BY USER
def add_hospital_account():
  from src.mail_services import send_email
  
  unique_code = check_redundant()

  if unique_code != None and send_email("Activation code", tambahan = unique_code) == True : return render_template("auth/register-succeed.html")
  # if register data found in database
  else: return render_template("auth/register.html", pesan = "That account already exist!")

# ADD NEW USER BY ADMIN
def admin_add_new_user(id):
  from read import get_id_account

  if request.method == 'POST':
    pm_key = check_redundant()

    if pm_key != None:
      # redirect to registered accounts or queue page
      if request.form['activate_status'] == 'Yes':
        db.child('akun_rs/' + pm_key +'/verified').set('Y')
        storage.child(pm_key + "/0.txt").put(os.path.join(os.path.dirname(os.path.abspath(__file__)), '0.txt'))
        return redirect(url_for('registered_accounts', id = get_id_account(id, sandi = True)))
      else:
        db.child('akun_rs/' + pm_key + '/verified').set(pm_key)
        return redirect(url_for('queue_account', id = get_id_account(id, sandi = True)))

    # if the data already exist
    else:
      return render_template("admins/add_new.html", id = get_id_account(id, sandi = True), pesan = "That account already exist!")

  return render_template("admins/add_new.html", id = get_id_account(id, sandi = True))