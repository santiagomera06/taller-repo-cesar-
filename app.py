from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google_recaptcha_flask import ReCaptcha

load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890aeiou"

#Cors para todas las rutas
CORS(app)

#conexión a Mongo Atlas
app.config["UPLOAD_FOLDER"] = "./static/imagenes"
app.config['MONGODB_SETTINGS'] = [{
    "db": "GestionPeliculas",
    "host": os.environ.get("URI")
     #"port": 27017
}]

#configurar recaptcha
app.config['GOOGLE_RECAPTCHA_ENABLED'] =True
app.config['GOOGLE_RECAPTCHA_SITE_KEY'] = os.environ.get("SITE-RECAPTCHA")  # Sustituye por tu clave pública
app.config['GOOGLE_RECAPTCHA_SECRET_KEY'] = os.environ.get("SECRET-RECAPTCHA") # Sustituye por tu clave secreta

#crear objeto detipo Recaptcha
recaptcha = ReCaptcha(app)

#Crear objeto de tipo MonoEngine
db = MongoEngine(app)

#importas las rutas
from routes.usuario import *
from routes.genero import *
from routes.pelicula import *

if __name__ == "__main__":    
    app.run(port=5000, host="0.0.0.0", debug=True)


