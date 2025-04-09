from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from models.usuario import Usuario
import random
import string
from extensions import mail

recuperar_bp = Blueprint('recuperar', __name__)

@recuperar_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar_contrasena():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        # Buscar usuario en la base de datos
        usuario = Usuario.objects(usuario=username, correo=email).first()

        if usuario:
            # Generar nueva contraseña
            caracteres = string.ascii_letters + string.digits
            nueva_contrasena = ''.join(random.choice(caracteres) for _ in range(8))

            # Actualizar contraseña en la base de datos
            usuario.update(password=nueva_contrasena)

            # Enviar correo con la nueva contraseña
            try:
                msg = Message('Recuperación de contraseña - Gestión Películas',
                             sender='santiagomera051@gmail.com',
                             recipients=[email])
                msg.body = f"""
                Hola {usuario.nombres} {usuario.apellidos},
                
                Se ha generado una nueva contraseña para tu cuenta en el sistema de Gestión de Películas.
                
                Tu nueva contraseña es: {nueva_contrasena}
                
                Por seguridad, te recomendamos cambiar esta contraseña después de iniciar sesión.
                
                Atentamente,
                El equipo de Gestión Películas
                """
                mail.send(msg)
                
                flash('Se ha enviado una nueva contraseña a tu correo electrónico.', 'success')
                return redirect(url_for('recuperar.recuperar_contrasena'))
            except Exception as e:
                flash(f'Error al enviar el correo: {str(e)}', 'danger')
        else:
            flash('Usuario o correo electrónico no encontrado.', 'danger')

    return render_template('recuperar.html')