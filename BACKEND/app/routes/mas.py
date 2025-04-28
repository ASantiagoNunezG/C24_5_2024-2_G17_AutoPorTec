#BACKEND/app/routes/mas.py
'''Aquí estarán las rutas para la parte de más, el reporte y la copia de seguridad'''

from flask import Blueprint, render_template

mas = Blueprint('mas', __name__)

#Endpoint para la página de más
@mas.route('/mas')
def more():
    return render_template('mas.html')