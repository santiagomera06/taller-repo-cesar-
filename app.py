from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from extensions import db, recaptcha

load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890aeiou"

# Configuración de MongoDB Atlas
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://santiagomera051:H5MPTVg7ssuOZCNB@cluster0.fdx1n.mongodb.net/GestionPelicula?retryWrites=true&w=majority&appName=Cluster0'
}

db.init_app(app)

# Configurar reCAPTCHA
app.config['GOOGLE_RECAPTCHA_ENABLED'] = True
app.config['GOOGLE_RECAPTCHA_SITE_KEY'] = os.environ.get("CLAVEDESITIO")
app.config['GOOGLE_RECAPTCHA_SECRET_KEY'] = os.environ.get("CLAVESECRETA")

recaptcha.init_app(app)

# Importar rutas
from routes.usuario import *
from routes.genero import *
from routes.pelicula import *



if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)