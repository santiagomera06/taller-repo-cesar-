from app import app
from flask import request, render_template, session
from models.genero import Genero
from models.pelicula import Pelicula


@app.route("/genero/", methods=['GET'])
def listGeneros():
    """_summary_
        Función que retorna la lista de generos
        existentes en la colección generos
    Returns:
        _type_: lista de generos
    """
    try:   
        mensaje=None     
        generos= Genero.objects()      
    
    except Exception as error:
        mensaje=str(error)
    
    return {"mensaje": mensaje, "generos":generos}


@app.route("/genero/", methods=['POST'])
def addGenero():
    try:
        mensaje=None
        estado=False
        if request.method=='POST':
            datos= request.get_json(force=True)       
            genero = Genero(**datos)      
            genero.save()
            estado=True
            mensaje="Genero agregado correctamente"  
        else:
            mensaje="No permitido"    
    except Exception as error:
        mensaje=str(error) 
        mensaje="Ya existe género con es nombre. Verficar."
        
    return {"estado":estado, "mensaje":mensaje}


        
@app.route("/genero/", methods=['PUT'])
def updateGenero():
    try:
        mensaje=None
        estado=False
        if request.method=='PUT':
            datos= request.get_json(force=True)
            genero = Genero.objects(id=datos['id']).first()
            genero.nombre = datos['nombre']
            genero.save()
            mensaje="Genero Actualizado"
            estado=True            
        else:
            mensaje="No permitido" 
    except Exception as error:
        mensaje=str(error)
        mensaje="No es posible actualizar. Ya existe un género con ese nombre"
        
    return {"estado":estado, "mensaje": mensaje}

@app.route("/genero/", methods=['DELETE'])
def deleteGenero():
    try:
        mensaje=None
        estado=True
        if request.method=="DELETE":
            datos=request.get_json(force=True)
            genero=Genero.objects(id=datos['id']).first()
            peliculas = Pelicula.objects()
            if (len(peliculas)>0):
                mensaje="No se puede eliminar. No permitido"
            else:
                if genero is None:
                    mensaje="Genero no encontrado. No se puede Eliminar"
                else:
                    genero.delete()
                    estado=True
                    mensaje="Genero Eliminado"
        else:
            mensaje="No permitido"  
    except Exception as error:
        mensaje=str(error)
        
    return {"estado": estado, "mensaje": mensaje}


#vistas

@app.route("/generos/", methods=['GET'])
def listarGeneros():
    try:
        mensaje=""
        generos=Genero.objects()        
    except Exception as error:
        mensaje=str(error)
    
    return render_template("listarGeneros.html",
                           generos=generos,mensaje=mensaje)
    
@app.route("/vistaGenero/", methods=['GET'])
def vistaGenero():
    return render_template("frmAgregarGenero.html")