from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google_recaptcha_flask import ReCaptcha

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890aeiou"

# Configuración de MongoDB Atlas
# Sustituye <db_password> con la contraseña de tu base de datos
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://santiagomera051:H5MPTVg7ssuOZCNB@cluster0.fdx1n.mongodb.net/GestionPelicula?retryWrites=true&w=majority&appName=Cluster0'
}

# Configurar reCAPTCHA
app.config['GOOGLE_RECAPTCHA_ENABLED'] = True
app.config['GOOGLE_RECAPTCHA_SITE_KEY'] = os.environ.get("CLAVEDESITIO")  # Sustituye por tu clave pública
app.config['GOOGLE_RECAPTCHA_SECRET_KEY'] = os.environ.get("CLAVESECRETA")  # Sustituye por tu clave secreta

# Crear objeto de tipo ReCaptcha
recaptcha = ReCaptcha(app)

# Crear objeto de tipo MongoEngine
db = MongoEngine(app)

# Importar rutas
from routes.usuario import *
from routes.genero import *
from routes.pelicula import *

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)


