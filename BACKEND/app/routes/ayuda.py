#BACKEND/app/routes/ayuda.py

#Aquí estarán las rutas para la parte de ayuda


from flask import Blueprint, render_template

ayuda = Blueprint('ayuda', __name__)

#Endpoint para la página de más
@ayuda.route('/ayuda')
def help():
    return render_template('ayuda.html')

@ayuda.route('/faq')
def preguntas_frecuentes():
    return render_template('centro_ayuda_templates/preguntas_frecuentes.html')

@ayuda.route('/contacto')
def soporte():
    return render_template('centro_ayuda_templates/soporte.html')