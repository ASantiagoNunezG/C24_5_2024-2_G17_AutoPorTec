#BACKEND/app/routes/pd_routes.py
'''Aquí estarán las rutas para la parte de carga del portafolio digital'''

from flask import Blueprint, render_template

carga_pd = Blueprint('carga_pd', __name__)

#Endpoint para la página del Portafolio Digital
@carga_pd.route('/pd')
def pd_carga():
    return render_template('carga_pd.html')