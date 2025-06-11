#BACKEND/app/routes/perfil.py
'''Aquí estarán las rutas para la parte del perfil'''

from flask import Blueprint, render_template, session, jsonify

perfil = Blueprint('perfil', __name__)

#Endpoint para la página del perfil
@perfil.route('/perfil')
def profile():
    user = session.get('user')  # obtenemos datos de usuario desde la sesión
    return render_template('perfil.html', user=user)


#Punto de prueba para ver los tokens que hay en session
"""
@perfil.route('/ver')
def ver_session():
    return jsonify(dict(session))
"""
