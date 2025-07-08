# BACKEND/app/routes/canvaslms.py


from flask import Blueprint, flash, request, session, redirect, url_for, render_template
from app.services.canvas_service import obtener_cursos, obtener_materiales_curso, quitar_token_service
from app.services.carpetas import switch_clasificacion_archivo
from app.services.google_drive_service import subir_archivo_a_drive
from app.services.estructura_portafolio_service import buscar_o_crear_carpeta, crear_o_obtener_carpeta_de_ruta, \
    estructura_portafolio_digital, crear_estructura_con_lookup
import mimetypes
import requests  # se importa por separado
from urllib.parse import unquote_plus

canvaslms = Blueprint('canvaslms', __name__)

@canvaslms.route('/canvas')
def canvas():
    if 'canvas_token' in session:
        return redirect(url_for('canvaslms.mostrar_cursos_guardado'))  # Nueva ruta para token en sesión

    return render_template('canvaslms.html')  # Formulario si no hay token

@canvaslms.route('/quitar-token')
def quitar_token():
    mensaje = quitar_token_service()
    if mensaje == 'Token de Canvas LMS eliminado correctamente':
        flash(mensaje, 'success')
    else:
        flash(mensaje, 'danger')
    return redirect(url_for('perfil.profile'))

@canvaslms.route('/canvas/cursos', methods=['POST'])
def mostrar_cursos():
    token = request.form.get('token')  # o request.args.get si es GET
    session.permanent = True # Activando el temporizador para el token de Canvas LMS
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


@canvaslms.route('/canvas/recopilar_material/<curso_id>', methods=['GET', 'POST'])
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

    carpeta_drive_id = buscar_o_crear_carpeta(google_token, nombre_carpeta, carpeta_padre_id)

    if not carpeta_drive_id:
        return "Error al crear carpeta en Drive", 500

    # Crear estructura de carpetas del portafolio y obtener IDs
    estructura = estructura_portafolio_digital()
    carpetas_ids = crear_estructura_con_lookup(google_token, carpeta_drive_id, estructura)

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
        carpeta_destino = switch_clasificacion_archivo(nombre_archivo)
        carpeta_id_destino = crear_o_obtener_carpeta_de_ruta(google_token, carpeta_destino, carpetas_ids, carpeta_drive_id)


        resultado = subir_archivo_a_drive(google_token, nombre_archivo, contenido, tipo_mime, carpeta_id_destino)
        if not resultado:
            return f"Error al subir el archivo: {nombre_archivo}", 500

    enlace = f"https://drive.google.com/drive/folders/{carpeta_drive_id}"
    return f"Material subido exitosamente. <a href='{enlace}' target='_blank'>Ver carpeta en Drive</a>"


