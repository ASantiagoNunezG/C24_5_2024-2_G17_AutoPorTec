#BACKEND/app/routes/perfil.py
'''Aquí estarán las rutas para la parte del perfil'''

from flask import Blueprint, render_template, session

perfil = Blueprint('perfil', __name__)

#Endpoint para la página del perfil
@perfil.route('/perfil')
def profile():
    user = session.get('user')  # obtenemos datos de usuario desde la sesión
    return render_template('perfil.html', user=user)