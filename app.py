# WEB FRAMEWORKS
from flask import Flask, render_template, redirect, request, url_for, session

# REFACTORED CODE
from src.db_storage.read import check_session, get_id_account, get_patients_data, data_users, user_dashboard, user_login
from src.db_storage.create import add_hospital_account, admin_add_new_user
from src.db_storage.delete import delete_session, delete_patient_data, delete_hospital_account
from src.db_storage.update import change_admin_pwd, change_patient_data, change_hospital_account, change_user_data, get_new_password, change_user_pwd

# FOR EMAIL SERVICES
from src.mail_services import send_email

# FOR DIAGNOSING
from src.model_serving.main_serve import diagnose_patient

# FLASK ROUTING AND SESSIONS
app = Flask(__name__)
app.secret_key = "rahasia"

# GENERAL - LANDING PAGE
@app.route('/')
def index():
  return (check_session() if session else render_template("index.html"))

# GENERAL - LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
  return (redirect('/') if session else user_login())

# GENERAL - REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
  return (add_hospital_account() if request.method == 'POST' else render_template("auth/register.html"))

# GENERAL - LOG OUT 
@app.route('/logout')
def logout():
  return (redirect('/') if session and delete_session() else redirect('/'))

# ADMIN - DASHBOARD
@app.route('/admin/<id>')
def dashboard_admin(id):
  return (render_template("admins/dashboard.html", id = get_id_account(id, sandi=True)) if session and id == session["admin"] else redirect('/'))

# ADMIN - CHANGE THE ADMIN PASSWORD
@app.route('/admin/<id>/changepwd', methods=['GET', 'POST'])
def change_pwd(id):
  return (redirect('/') if session and id == session["admin"] and request.method == 'POST' and change_admin_pwd(id) else redirect('/'))

# ADMIN - SEE THE REGISTERED ACCOUNT
@app.route('/admin/<id>/registered_accounts', methods=['GET', 'POST'])
def registered_accounts(id):
  return (render_template("admins/registered_accounts.html", id = get_id_account(id, sandi=True), data = data_users()) if session and id == session["admin"] else redirect('/')) 

# ADMIN - ADD NEW ACCOUNT/USER
@app.route('/admin/<id>/add_new', methods=['GET', 'POST'])
def add_new_account(id):
  return (admin_add_new_user(id) if session and id == session["admin"] else redirect('/'))

# ADMIN - SEE THE INACTIVE USER
@app.route('/admin/<id>/queue')
def queue_accounts(id):
  return (render_template("admins/registered_accounts.html", id = get_id_account(id, sandi=True), data = data_users(verified='N')) if session and id == session["admin"] else redirect('/'))

# ADMIN - EDIT THE USER ACCOUNT
@app.route('/edit_user/<id>/<id_user>', methods=['GET', 'POST'])
def edit_user(id, id_user):
  return (change_hospital_account(id, id_user) if session and id == session['admin'] else redirect('/')) 

# ADMIN - DELETE THE USER ACCOUNT
@app.route('/delete_user/<id>/<id_user>')
def delete_user(id, id_user):
  return (redirect('/') if session and id == session['admin'] and delete_hospital_account(id_user) else redirect('/'))

# USER - DASHBOARD
@app.route('/user/<id>', methods=['GET', 'POST'])
def dashboard_user(id):
  return (user_dashboard(id) if session and id == session["user"] else redirect('/'))

# USER - GET NEW PASSWORD
@app.route('/reset-pwd', methods=['GET', 'POST'])
def reset_pwd():
  return (get_new_password() if request.method == 'POST' else render_template("auth/forgot-password.html"))

# USER - RESET PASSWORD
@app.route('/reset-pwd/new-pwd', methods=['GET', 'POST'])
def new_pwd():
  return (change_user_pwd() if request.method == 'POST' else render_template("auth/new_pwd.html"))

# USER - RESEND UNIQUE CODE TO ACTIVAE THE ACCOUNT
@app.route('/resend/<id>')
def resend(id):
  if send_email("Activation Code", id=id): return redirect(url_for('dashboard_user', id=id))

# USER - SEND THE ISSUE THAT FOUND BY THE USER
@app.route('/complaint/<id>', methods=['GET', 'POST'])
def user_complaint(id):
  return (redirect('/') if session and id == session['user'] and request.method == 'POST' and send_email('User complaint', id=id) else redirect('/'))

# USER - EDIT THE USER DATA
@app.route('/user_edit_data/<id>', methods=['GET', 'POST'])
def user_edit_data(id):
  return (change_user_data(id) if session and id == session['user'] and request.method == 'POST' else redirect('/'))

# USER - DIAGNOSING
@app.route('/diagnose/<id>/', methods=['GET', 'POST'])
def diagnose(id):
  return (diagnose_patient(id) if session and id == session['user'] else redirect('/'))

# USER - SEE THE DIAGNOSED PATIENTS
@app.route('/diagnosed/<id>/<disease>')
def diagnosed(id, disease):
  return (render_template('users/diagnosed_list.html', id = get_id_account(id), data = get_patients_data(id, disease), disease = disease) if session and id == session['user'] else redirect('/'))

# USER - EDIT PATIENT DATA
@app.route('/edit_patient/<id>/<disease>/<id_patient>', methods=['GET', 'POST'])
def edit_patient(id, disease, id_patient):
  return (change_patient_data(id, disease, id_patient) if session and id == session['user'] else redirect('/'))

# USER - DELETE PATIENT DATA
@app.route('/delete_patient/<id>/<disease>/<id_patient>')
def delete_patient(id, disease, id_patient):
  return (redirect(url_for('diagnosed', id = id, disease = disease)) if session and id == session['user'] and delete_patient_data(id, disease, id_patient) else redirect('/'))

# ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
  return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
  return render_template('error/500.html'), 500

#app.run(debug=True)
