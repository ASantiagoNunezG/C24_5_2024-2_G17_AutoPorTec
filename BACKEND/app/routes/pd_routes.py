#BACKEND/app/routes/pd_routes.py
'''Aquí estarán las rutas para la parte de carga del portafolio digital'''

from flask import Blueprint, render_template, session

from app.services.google_drive_service import upload_to_drive
from app.services.zip_service import crear_zip_en_memoria

carga_pd = Blueprint('carga_pd', __name__)

#Endpoint para la página del Portafolio Digital
@carga_pd.route('/pd')
def pd_carga():
    return render_template('carga_pd.html')
'''
@carga_pd.route('/subir_zip_drive')
def subir_zip_a_drive():
    access_token = session.get('google_token', {}).get('access_token')
    if not access_token:
        return "No estás autenticado", 401

    # Crear ZIP en memoria (BytesIO)
    archivo_zip = crear_zip_en_memoria(materiales)
    archivo_zip.seek(0)  # Muy importante: volver al inicio del stream

    resultado = upload_to_drive(access_token, archivo_zip, carpeta_nombre + '.zip')

    if resultado:
        return f"Archivo subido con éxito. ID de Drive: {resultado['id']}"
    else:
        return "Error subiendo archivo a Google Drive", 500
'''