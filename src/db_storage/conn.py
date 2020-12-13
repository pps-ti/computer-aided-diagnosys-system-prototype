from pyrebase import initialize_app

config = {
  "apiKey": "rahasia",
  "authDomain": "rahasia",
  "databaseURL": "rahasia",
  "projectId": "rahasia",
  "storageBucket": "rahasia",
  "messagingSenderId": "rahasia",
  "appId": "rahasia",
  "serviceAccount" : {
    "type": "service_account",
    "project_id": "rahasia",
    "private_key_id": "rahasia",
    "private_key": "rahasia",
    "client_email": "rahasia",
    "client_id": "rahasia",
    "auth_uri": "rahasia",
    "token_uri": "rahasia",
    "auth_provider_x509_cert_url": "rahasia",
    "client_x509_cert_url": "rahasia"
  }
}

db = initialize_app(config).database()
storage = initialize_app(config).storage()