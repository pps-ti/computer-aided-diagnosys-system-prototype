import sys, os
import joblib
import numpy as np
from skimage import io, transform

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join('../../..', 'src')))

from db_storage.conn import storage # DATABASE CONNECTION

# LAPISAN PADA CNN
from conv import Conv3x3
from maxpool import MaxPool2

hasil_klasifikasi = lambda x : (np.exp(x)/np.sum(np.exp(x)), np.argmax(np.exp(x)/np.sum(np.exp(x))))

def hybrid_cnn_elm(title):
  conv = Conv3x3(8)
  pool = MaxPool2()
  
  elm_model = joblib.load('models/hybrid/hybrid.pkl')

  # PRAPROSES CITRA
  gambar = transform.resize(io.imread(storage.child(title[0]).get_url(None), as_gray=True), (50, 50))
  gambar = (gambar-0)*(1-0)/(255-0)+0

  # PROSES PADA CNN
  gambar = conv.forward((gambar / 255) - 0.5)
  gambar = np.maximum(gambar, 0, gambar) # ReLU
  gambar = pool.forward(gambar)

  # UBAH CITRA YANG TERKESTRAKSI KE DALAM BENTUK VEKTOR
  gambar = np.ravel(gambar)

  # PROSES PADA ELM
  gambar = np.dot(gambar, elm_model['win'])
  gambar += elm_model['bias']
  gambar = 1/(1 + np.exp(-gambar)) # SIGMOID

  # OUTPUT
  hasil = hasil_klasifikasi(np.dot(gambar, elm_model['wout']))

  proba = {"Tumor existance" : str(hasil[0][0]), "Healthy brain" : str(hasil[0][1])}
  hasil_diagnosa = 'Indicated Brain Tumor' if hasil[1] == 0 else 'Not Indicated Brain Tumor'

  # NILAI KEMBALIAN BERUPA PROBABILITAS DAN HASIL DIAGNOSA
  return proba, hasil_diagnosa