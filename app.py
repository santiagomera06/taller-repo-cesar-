from flask import Flask, render_template
from flask_mongoengine import MongoEngine

app = Flask(__name__)

#cadena de conexión base datos en mongoatlas
uri="mongodb+srv://cesarmcuellar:12345@runt.oudoapr.mongodb.net/?retryWrites=true&w=majority&appName=RUNT"

app.config["UPLOAD_FOLDER"] = "./static/imagenes"
app.config['MONGODB_SETTINGS'] = [{
    "db": "GestionPeliculas",
    "host": uri
     #"port": 27017
}]
db = MongoEngine(app)

@app.route("/")
def inicio():
    return render_template("contenido.html")

if __name__ == "__main__":
    from routes.genero import *
    from routes.pelicula import *
    app.run(port=5000, host="0.0.0.0", debug=True)


