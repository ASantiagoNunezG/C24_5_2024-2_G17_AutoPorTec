# BACKEND/app/routes/canvaslms.py
from flask import Blueprint, render_template, request,  send_file, session, redirect, url_for, render_template
from app.services.canvas_service import obtener_cursos, obtener_materiales_curso
from app.services.estructura_portafolio_service import crear_estructura_portafolio_drive
from app.services.google_drive_service import crear_carpeta_drive, subir_archivo_a_drive
import mimetypes
import requests  # se importa por separado
from urllib.parse import unquote_plus

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
    canvas_token = session.get('canvas_token')
    google_token = session.get('google_token', {}).get('access_token')

    if not canvas_token:
        return "Token de Canvas no disponible. Por favor, vuelve a ingresar tu token.", 403
    if not google_token:
        return "No estás autenticado con Google Drive.", 401

    nombre_carpeta = request.form.get('carpeta_nombre', curso_id)
    materiales = obtener_materiales_curso(canvas_token, curso_id)
    if not materiales:
        return "No se encontraron materiales para este curso", 404

    
    folder_id = session.get('drive_folder_id')
    if folder_id:
        carpeta_padre_id = folder_id
    else:
        carpeta_padre_id = 'root'

    carpeta_drive_id = crear_carpeta_drive(google_token, nombre_carpeta, parent_id=carpeta_padre_id)

    if not carpeta_drive_id:
        return "Error al crear carpeta en Drive", 500

    # Crear estructura de carpetas del portafolio y obtener IDs
    from app.services.estructura_portafolio_service import clasificar_archivo
    carpetas_ids = crear_estructura_portafolio_drive(google_token, carpeta_drive_id)

    # Subir archivos a la carpeta según clasificación
    for material in materiales:
        nombre_archivo = unquote_plus(material['filename'])
        archivo_url = material['url']

        headers = {'Authorization': f'Bearer {canvas_token}'}
        respuesta = requests.get(archivo_url, headers=headers)
        if respuesta.status_code != 200:
            print(f"Error descargando archivo: {archivo_url} - {respuesta.status_code}")
            continue

        contenido = respuesta.content
        tipo_mime, _ = mimetypes.guess_type(nombre_archivo)
        if not tipo_mime:
            tipo_mime = 'application/octet-stream'

        # Clasificar archivo para saber carpeta destino
        carpeta_destino = clasificar_archivo(nombre_archivo)
        carpeta_id_destino = carpetas_ids.get(carpeta_destino) or carpetas_ids.get('Material Complementario')

        resultado = subir_archivo_a_drive(google_token, nombre_archivo, contenido, tipo_mime, carpeta_id_destino)
        if not resultado:
            return f"Error al subir el archivo: {nombre_archivo}", 500

    enlace = f"https://drive.google.com/drive/folders/{carpeta_drive_id}"
    return f"Material subido exitosamente. <a href='{enlace}' target='_blank'>Ver carpeta en Drive</a>"
