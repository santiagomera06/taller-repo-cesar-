from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890aeiou"

#cadena de conexión base datos en mongoatlas
user=os.environ.get("USER-BD")
password = os.environ.get("PASSWORD-BD")
uri=f"mongodb+srv://{user}:{password}@runt.oudoapr.mongodb.net/?retryWrites=true&w=majority&appName=RUNT"
app.config["UPLOAD_FOLDER"] = "./static/imagenes"
app.config['MONGODB_SETTINGS'] = [{
    "db": "GestionPeliculas",
    "host": uri
     #"port": 27017
}]
app.config['CORS_HEADERS'] = 'Content-Type'

db = MongoEngine(app)


from routes.usuario import *
from routes.genero import *
from routes.pelicula import *
if __name__ == "__main__":
    
    app.run(port=5000, host="0.0.0.0", debug=True)


