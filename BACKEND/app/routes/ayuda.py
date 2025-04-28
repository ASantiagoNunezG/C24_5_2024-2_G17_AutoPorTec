#BACKEND/app/routes/ayuda.py
'''Aquí estarán las rutas para la parte de ayuda'''

from flask import Blueprint, render_template

ayuda = Blueprint('ayuda', __name__)

#Endpoint para la página de más
@ayuda.route('/ayuda')
def help():
    return render_template('ayuda.html')