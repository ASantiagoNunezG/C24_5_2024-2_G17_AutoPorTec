#BACKEND/app/routes/ajustes.py
'''Aquí estarán las rutas para la parte de ajustes'''

from flask import Blueprint, render_template

ajustes = Blueprint('ajustes', __name__)

#Endpoint para la página de ajustes
@ajustes.route('/ajustes')
def config():
    return render_template('ajustes.html')