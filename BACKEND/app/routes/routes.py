#BACKEND/app/routes/routes.py
'''Aquí están las rutas para el home y la página de errores'''
from flask import Blueprint,render_template

home_bp = Blueprint('home', __name__)

#Endpoint para la página de inicio
@home_bp.route('/')
def inicio():
    return render_template('home.html')
    #también se puede hacer un redirect para que vaya al login

# Endpoint para la página de error de nivel global
@home_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404