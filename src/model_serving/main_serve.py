import os, sys

from flask import request, render_template
from werkzeug.utils import secure_filename

import joblib
import numpy as np
from PIL import Image
from torch import load
from torchvision import transforms

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join('../..', 'src')))

from mail_services import send_diagnose_result
from db_storage.conn import db, storage
from db_storage.read import get_id_account
from tumor_otak.model import hybrid_cnn_elm, hasil_klasifikasi

# UNTUK MENDAPATKAN NAMA FILE DAN ID PASIEN
def get_patient_id_title(id):
  from random import choice
  from string import ascii_uppercase, digits

  patient_id = ''.join(choice(ascii_uppercase + digits) for _ in range(8))

  storage.child(id + '/'+ request.form['disease'] + '/' + patient_id + '.' + secure_filename(request.files['image'].filename).split('.')[-1]).put(request.files['image'])
  title = [data.name for data in storage.list_files() if id + '/' + request.form['disease'] + '/' + patient_id in data.name]
  
  return patient_id, title

# COLON TISSUE - UNTUK MENDAPATKAN HASIL DIAGNOSA
def colon_tissue(hasil_klasifikasi):
  proba = {"Cancer existance on the tissue" : str(hasil_klasifikasi[0][0][0]),
           "Healthy colon tissue" : str(hasil_klasifikasi[0][0][1])}
  hasil_diagnosa = 'Indicated Colon Cancer' if hasil_klasifikasi[1] == 0 else 'Not Indicated Colon Cancer'

  return proba, hasil_diagnosa

# LUNG TISSUE - UNTUK MENDAPATKAN HASIL DIAGNOSA
def lung_tissue(hasil_klasifikasi):
  proba = {"Inicated Adenocarcinoma Cancer" : str(hasil_klasifikasi[0][0][0]),
           "Not Indicated Lung Cancer" : str(hasil_klasifikasi[0][0][1]),
           "Inicated Squamous Carcinoma Cancer" : str(hasil_klasifikasi[0][0][2])}
  
  if hasil_klasifikasi[1] == 0: hasil_diagnosa = 'Indicated Adenocarcinoma Cancer'
  elif hasil_klasifikasi[1] == 1: hasil_diagnosa = 'Not Indicated Lung Cancer'
  else: hasil_diagnosa = 'Indicated Squamous Carcinoma Cancer'

  return proba, hasil_diagnosa

# MALARIA - UNTUK MENDAPATKAN HASIL DIAGNOSA
def malaria(hasil_klasifikasi):
  proba = {"Malaria existance on blood" : str(hasil_klasifikasi[0][0][0]),
           "Healthy blood" : str(hasil_klasifikasi[0][0][1])}
  
  hasil_diagnosa = 'Indicated Malaria' if hasil_klasifikasi[1] == 0 else 'Not Indicated Malaria'
  
  return proba, hasil_diagnosa

# PARKINSON - UNTUK MENDAPATKAN HASIL DIAGNOSA
def parkinson(hasil_klasifikasi):
  proba = {"Indicated Parkinson" : str(hasil_klasifikasi[0][0][0]),
           "Not Indicated Parkinson" : str(hasil_klasifikasi[0][0][1])}
  
  hasil_diagnosa = 'Indicated Parkinson' if hasil_klasifikasi[1] == 0 else 'Not Indicated Parkinson'
  
  return proba, hasil_diagnosa

# RETINA OCT - UNTUK MENDAPATKAN HASIL DIAGNOSA
def retina_oct(hasil_klasifikasi):
  proba = {"Inicated Choroidal Neovascularization" : str(hasil_klasifikasi[0][0][0]),
           "Inicated Diabetic Macular Edema" : str(hasil_klasifikasi[0][0][1]),
           "Inicated Drusen" : str(hasil_klasifikasi[0][0][2]),
           "Healty Retina" : str(hasil_klasifikasi[0][0][3])}
  
  if hasil_klasifikasi[1] == 0: hasil_diagnosa = 'Indicated Choroidal Neovascularization'
  elif hasil_klasifikasi[1] == 1: hasil_diagnosa = 'Indicated Diabetic Macular Edema'
  elif hasil_klasifikasi[1] == 2: hasil_diagnosa = 'Indicated Drusen'
  else: hasil_diagnosa = 'Not Indicated Any Disease'
  
  return proba, hasil_diagnosa

# UNTUK MENAMBAHKAN DATA KE FIREBASE
def add_to_firebase(proba, hasil, id, patient_id, title):
  db.child('akun_rs/' + id +'/patients_data/' + request.form['disease'] + '/' + patient_id).set({
    'address' : request.form['address'],
    'name' : request.form['name'],
    'birth_date' : request.form['birth_date'],
    'email' : request.form['email'],
    'gender' : request.form['gender'],
    'height' : request.form['height'],
    'weight' : request.form['weight'],
    'blood_type' : request.form['blood_type'],
    'result' : hasil, 'proba' : proba,
    'image' : storage.child(title[0]).get_url(None)
  })

  #storage.delete(title[0])

# FUNGSI UTAMA
def diagnose_patient(id):
  if request.method == 'POST':
    patient_id, title = get_patient_id_title(id); global hasil_klasifikasi

    if request.form['disease'] != 'brain_tumor':
      model = load('models/' + request.form['disease'] + '.pt', map_location='cpu')
      model.eval()

      image_size = 100 if request.form['disease'] == 'malaria' else 224

      normalize = transforms.Compose([transforms.Resize((image_size, image_size)),
                                      transforms.ColorJitter(0.05),
                                      transforms.ToTensor(),
                                      transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])

      if request.form['disease'] != 'retina_oct':
        hasil_klasifikasi = hasil_klasifikasi(model(normalize(Image.open(request.files['image'])).view(-1, 3, image_size, image_size)).detach().numpy())
      
      else:
        img = Image.open(request.files['image'])
        rgbimg = Image.new("RGB", img.size)
        rgbimg.paste(img)
        print(type(rgbimg))

        hasil_klasifikasi = hasil_klasifikasi(model(normalize(rgbimg).view(-1, 3, image_size, image_size)).detach().numpy())
        proba, hasil_diagnosa = retina_oct(hasil_klasifikasi)

      if request.form['disease'] == 'colon_tissue': proba, hasil_diagnosa = colon_tissue(hasil_klasifikasi)
      elif request.form['disease'] == 'lung_tissue': proba, hasil_diagnosa = lung_tissue(hasil_klasifikasi)  
      elif request.form['disease'] == 'malaria': proba, hasil_diagnosa = malaria(hasil_klasifikasi)
      elif request.form['disease'] == 'parkinson': proba, hasil_diagnosa = parkinson(hasil_klasifikasi)

    else: proba, hasil_diagnosa = hybrid_cnn_elm(title)

    send_diagnose_result(proba=proba, image=storage.child(title[0]).get_url(None), hasil = hasil_diagnosa)
    add_to_firebase(proba, hasil_diagnosa, id, patient_id, title)
    result = dict(db.child('akun_rs/' + id + '/patients_data/' + request.form['disease'] + '/' + patient_id + '/').get().val())

    return render_template('users/diagnose_result.html', id = get_id_account(id), result = result)
  return render_template('users/diagnose.html', id = get_id_account(id))