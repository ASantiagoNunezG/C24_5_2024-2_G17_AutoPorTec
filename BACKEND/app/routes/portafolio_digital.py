# BACKEND/app/routes/portafolio_digital.py
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

portafolio_digital = Blueprint('portafoliod', __name__)

@portafolio_digital.get('/portafoliod')
def portafolio():
    google_token = session.get('google_token', {}).get('access_token')
    return render_template('portafolio_digital.html',token=google_token, api_key=GOOGLE_API_KEY)

#Guardar el Id de la carpeta
@portafolio_digital.route('/save-folder', methods=['POST'])
def save_folder():
    folder_id = request.form.get('folderId')  # ← importante
    folder_name = request.form.get('folderName')

    if folder_id:
        session['drive_folder_id'] = folder_id
        flash(f"✅ Carpeta [{folder_name}] seleccionada correctamente", "success")
    else:
        flash("❌ No se recibió el ID de la carpeta", "error")

    return redirect(url_for('portafoliod.portafolio'))