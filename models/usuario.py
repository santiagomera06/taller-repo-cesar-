from mongoengine import *
#from app import db

class Usuario(Document):
    usuario = StringField(max_length=50, required=True, unique=True)
    password = StringField(max_length=50,required=True)
    nombres = StringField(max_length=50,required=True)
    apellidos = StringField(max_length=50,required=True)
    correo = EmailField(required=True, unique=True)



