from app import app
from flask import request, render_template, redirect, session
from models.pelicula import Pelicula
from models.genero import Genero
from bson.objectid import ObjectId

from werkzeug.utils import secure_filename
import os

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/pelicula/", methods=['GET'])
def listPelicula():
    try:   
        mensaje=None     
        peliculas= Pelicula.objects()  
    except Exception as error:
        mensaje=str(error)
    
    return {"mensaje": mensaje, "peliculas":peliculas}

@app.route("/pelicula/", methods=['POST'])
def addPelicula():
    try:
        mensaje = None
        estado = False
        
        if request.method == "POST":
            # Verificar si ya existe una película con el mismo código
            codigo = request.form['txtCodigo']
            existe_pelicula = Pelicula.objects(codigo=codigo).first()
            if existe_pelicula:
                return {"estado": False, "mensaje": "Ya existe una película con ese código"}
            
            # Procesar los datos del formulario
            titulo = request.form['txtTitulo']
            duracion = request.form['txtDuracion']
            protagonista = request.form['txtProtagonista']
            genero_id = request.form['cbGenero']
            resumen = request.form['txtResumen']
            
            # Validar género
            genero = Genero.objects(id=genero_id).first()
            if not genero:
                return {"estado": False, "mensaje": "Género no válido"}
            
            # Procesar la imagen
            nombreFotoServidor = None
            if 'fileFoto' in request.files:
                foto = request.files['fileFoto']
                if foto.filename != '':
                    if not allowed_file(foto.filename):
                        return {"estado": False, "mensaje": "Formato de imagen no permitido"}
                    
                    filename = secure_filename(foto.filename)
                    extension = filename.rsplit('.', 1)[1].lower()
                    nombreFotoServidor = f"pelicula_{codigo}.{extension}"
                    rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nombreFotoServidor)
                    foto.save(rutaFoto)
            
            # Crear y guardar la película
            pelicula = Pelicula(
                codigo=codigo,
                titulo=titulo,
                duracion=duracion,
                protagonista=protagonista,
                genero=genero,
                resumen=resumen,
                foto=nombreFotoServidor
            )
            pelicula.save()
            
            estado = True
            mensaje = "Película agregada correctamente"
            
    except Exception as error:
        mensaje = f"Error al agregar la película: {str(error)}"
        
    return {"estado": estado, "mensaje": mensaje}


@app.route("/pelicula/", methods=['PUT'])
def updatePelicula():
    try:
        mensaje = None
        estado = False
        
        if request.method == 'PUT':
            # Obtener datos del formulario
            id_pelicula = request.form['id']
            codigo = request.form['txtCodigo']
            
            # Obtener la película a actualizar
            pelicula = Pelicula.objects(id=ObjectId(id_pelicula)).first()
            if not pelicula:
                return {"estado": False, "mensaje": "Película no encontrada"}
            
            # Verificar si el nuevo código ya existe en otra película
            if codigo != pelicula.codigo:
                existe_pelicula = Pelicula.objects(codigo=codigo).first()
                if existe_pelicula:
                    return {"estado": False, "mensaje": "Ya existe una película con ese código"}
            
            # Actualizar campos básicos
            pelicula.codigo = codigo
            pelicula.titulo = request.form['txtTitulo']
            pelicula.duracion = request.form['txtDuracion']
            pelicula.protagonista = request.form['txtProtagonista']
            pelicula.resumen = request.form['txtResumen']
            
            # Actualizar género
            genero_id = request.form['cbGenero']
            genero = Genero.objects(id=genero_id).first()
            if genero:
                pelicula.genero = genero
            
            # Manejar la imagen
            if 'fileFoto' in request.files:
                foto = request.files['fileFoto']
                if foto.filename != '':
                    # Eliminar la imagen anterior si existe
                    if pelicula.foto:
                        try:
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pelicula.foto))
                        except:
                            pass
                    
                    # Guardar la nueva imagen
                    filename = secure_filename(foto.filename)
                    extension = filename.rsplit('.', 1)[1].lower()
                    nombreFotoServidor = f"pelicula_{codigo}.{extension}"
                    rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nombreFotoServidor)
                    foto.save(rutaFoto)
                    pelicula.foto = nombreFotoServidor
            
            pelicula.save()
            estado = True
            mensaje = "Película actualizada correctamente"
            
    except Exception as error:
        mensaje = f"Error al actualizar la película: {str(error)}"
        
    return {"estado": estado, "mensaje": mensaje}
@app.route("/pelicula/", methods=['DELETE'])
def deletePelicula():
    try:
        mensaje = None
        estado = False
        if request.method == "DELETE":
            datos = request.get_json(force=True)
            pelicula = Pelicula.objects(id=datos['id']).first()
            
            if pelicula is None:
                mensaje = "No existe película con ese ID"
            else:
                # Eliminar la imagen asociada si existe
                if pelicula.foto:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pelicula.foto))
                    except:
                        pass
                
                pelicula.delete()
                estado = True
                mensaje = "Película eliminada correctamente"
        else:
            mensaje = "Método no permitido"
            
    except Exception as error:
        mensaje = f"Error al eliminar la película: {str(error)}"
        
    return {"estado": estado, "mensaje": mensaje}
#vistas

@app.route("/peliculas/", methods=['GET'])
def listarPeliculas():
    if ("user" in session):
        peliculas = Pelicula.objects()
        generos = Genero.objects()
        print(generos)
        return render_template("listarPeliculas.html", 
                            peliculas=peliculas,
                            generos=generos)
    else:
        mensaje="Debe primero ingresar con credenciales válidas"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)
        


@app.route("/vistaAgregarPelicula/", methods=['GET', 'POST'])
def vistaAgregarPelicula():
    if "user" not in session:
        mensaje = "Debe primero ingresar con credenciales válidas"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)
    
    if request.method == 'GET':
        generos = Genero.objects()
        return render_template("frmAgregarPelicula.html", generos=generos)
    
    elif request.method == 'POST':
        try:
            codigo = request.form['txtCodigo']
            titulo = request.form['txtTitulo']
            duracion = request.form['txtDuracion']
            protagonista = request.form['txtProtagonista']
            genero_id = request.form['cbGenero']
            resumen = request.form['txtResumen']
            foto = request.files['fileFoto']
            
            genero = Genero.objects(id=genero_id).first()
            if not genero:
                return render_template("frmAgregarPelicula.html", 
                                    generos=Genero.objects(),
                                    mensaje="Género no válido")
            
            # Procesar la imagen
            if foto and allowed_file(foto.filename):
                filename = secure_filename(foto.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                nombreFotoServidor = f"pelicula_{codigo}.{extension}"
                rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nombreFotoServidor)
                foto.save(rutaFoto)
            else:
                nombreFotoServidor = None
            
            pelicula = Pelicula(
                codigo=codigo,
                titulo=titulo,
                duracion=duracion,
                protagonista=protagonista,
                genero=genero,
                resumen=resumen,
                foto=nombreFotoServidor
            )
            pelicula.save()
            
            return redirect("/peliculas/")
            
        except Exception as error:
            return render_template("frmAgregarPelicula.html", 
                                generos=Genero.objects(),
                                mensaje=str(error))
        

@app.route("/vistaEditarPelicula/<string:id>/", methods=['GET', 'POST'])
def mostrarVistaEditarPelicula(id):  
    if "user" not in session:
        mensaje = "Debe primero ingresar con credenciales válidas"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)
    
    pelicula = Pelicula.objects(id=ObjectId(id)).first()
    if not pelicula:
        return redirect("/peliculas/")
    
    if request.method == 'GET':
        generos = Genero.objects()
        return render_template("frmEditarPelicula.html",
                            pelicula=pelicula, generos=generos)
    
    elif request.method == 'POST':
        try:
            pelicula.codigo = request.form['txtCodigo']
            pelicula.titulo = request.form['txtTitulo']
            pelicula.duracion = request.form['txtDuracion']
            pelicula.protagonista = request.form['txtProtagonista']
            pelicula.resumen = request.form['txtResumen']
            
            genero_id = request.form['cbGenero']
            genero = Genero.objects(id=genero_id).first()
            if genero:
                pelicula.genero = genero
            
            foto = request.files['fileFoto']
            if foto and allowed_file(foto.filename):
                # Eliminar la foto anterior si existe
                if pelicula.foto:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pelicula.foto))
                    except:
                        pass
                
                # Guardar la nueva foto
                filename = secure_filename(foto.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                nombreFotoServidor = f"pelicula_{pelicula.codigo}.{extension}"
                rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nombreFotoServidor)
                foto.save(rutaFoto)
                pelicula.foto = nombreFotoServidor
            
            pelicula.save()
            
            return redirect("/peliculas/")
            
        except Exception as error:
            generos = Genero.objects()
            return render_template("frmEditarPelicula.html",
                                pelicula=pelicula, generos=generos,
                                mensaje=str(error))
   
