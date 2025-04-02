from app import app,db
from flask import Flask, render_template, request, jsonify, session, redirect
from flask_mongoengine import MongoEngine
from models.usuario import Usuario
import urllib
import json




@app.route("/")
def inicio():
    return render_template("frmIniciarSesion.html")


@app.route("/iniciarSesion/",  methods=['POST'])
def iniciarSesion():   
        mensaje = ""
        if request.method=='POST':
            try:
                # validar el recapthcha
                """Begin reCAPTCHA validation"""
                recaptcha_response = request.form['g-recaptcha-response']
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': '6LdYkgYrAAAAAJ9Wmt8S-YMA5dVCmspqTCHtlXUI',  # la clave secreta
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                # End reCAPTCHA validation """
                print(result)
                if result['success']:   
                    print("Ingresé")        
                    username=request.form['txtUser']
                    password=request.form['txtPassword'] 
                    usuario = Usuario.objects(usuario=username,password=password).first()
                    if usuario:
                        print("hay usuario")
                        session['user']=username
                        print(session['user'])
                        return render_template("contenido.html")
                    else:
                        mensaje="Credenciales no válidas"
                else:
                    mensaje = "Debe validar primero el recaptcha"
              
            except Exception as error:
                mensaje=str(error)
    
            return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route("/usuario/", methods=['POST'])
def addUsuario():
    try:
        mensaje=None
        estado=False
        datos= request.get_json(force=True)
        usuario = Usuario(**datos)
        usuario.save()
        estado=True
        mensaje="Usuario agregado correctamente"       
        
    except Exception as error:
        mensaje=str(error) 
        
    return {"estado":estado, "mensaje":mensaje}

@app.route("/salir/")
def exit():
    session.clear()
    mensaje="Ha cerrado la sesión de forma"
    return render_template("frmIniciarSesion.html",mensaje=mensaje)