# BACKEND/app/routes/canvaslms.py
from flask import Blueprint, render_template, request, send_file, session, redirect, url_for, render_template
from app.services.canvas_service import obtener_cursos, obtener_materiales_curso
from app.services.google_drive_service import upload_to_drive
from app.services.zip_service import crear_zip_en_memoria

canvaslms = Blueprint('canvaslms', __name__)

@canvaslms.route('/canvas')
def canvas():
    if 'canvas_token' in session:
        return redirect(url_for('canvaslms.mostrar_cursos_guardado'))  # Nueva ruta para token en sesión

    return render_template('canvaslms.html')  # Formulario si no hay token


@canvaslms.route('/canvas/cursos', methods=['POST'])
def mostrar_cursos():
    token = request.form.get('token')  # o request.args.get si es GET

    # Guarda el token en la sesión del usuario
    session['canvas_token'] = token

    cursos = obtener_cursos(token)

    if cursos is not None:
        return render_template('canvaslms2.html', cursos=cursos, token=token)
    else:
        return render_template('canvaslms2.html', error="No se pudo obtener los cursos")


@canvaslms.route('/mostrar_cursos_guardado', methods=['GET'])
def mostrar_cursos_guardado():
    token = session.get('canvas_token')
    if not token:
        return redirect(url_for('canvaslms.canvas'))  # Si no hay token, vuelve al formulario

    cursos = obtener_cursos(token)
    return render_template('canvaslms2.html', cursos=cursos)


@canvaslms.route('/canvas/recopilar_material/<curso_id>', methods=['POST'])
def recopilar_material_ruta(curso_id):

    canvas_token = session.get('canvas_token')  # Recupera el token seguro
    google_token = session.get('google_token', {}).get('access_token')

    if not canvas_token:
        return "Token de Canvas no disponible. Por favor, vuelve a ingresar tu token.", 403
    if not google_token:
        return "No estás autenticado con Google Drive.", 401

    # Nombre de la carpeta / archivo
    carpeta_nombre = request.form.get('carpeta_nombre', curso_id)

    # Obtener materiales del curso Canvas
    materiales = obtener_materiales_curso(canvas_token, curso_id)
    if not materiales:
        return "No se encontraron materiales para este curso", 404

    # Crear ZIP en memoria
    archivo_zip = crear_zip_en_memoria(materiales)
    archivo_zip.seek(0)

    folder_id = '1V5vDQpMJzdeSX31zjp8QJPw_NQcrUGPv'  # ID real de tu carpeta

    # Subir a Google Drive
    resultado = upload_to_drive(google_token, archivo_zip, carpeta_nombre + '.zip', folder_id)

    if resultado:
        return f"Archivo subido con éxito a Google Drive. ID: {resultado['id']}"
    else:
        return "Error subiendo archivo a Google Drive", 500


