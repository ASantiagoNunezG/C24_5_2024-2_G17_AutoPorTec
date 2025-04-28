# BACKEND/app/routes/canvaslms.py
from flask import Blueprint, render_template, request, send_file
from app.services.canvas_service import obtener_cursos, obtener_materiales_curso
from app.services.material_service import recopilar_material
import os

canvaslms = Blueprint('canvaslms', __name__)

@canvaslms.route('/canvas')
def canvas():
    return render_template('canvaslms.html')


@canvaslms.route('/canvas/cursos', methods=['POST'])
def mostrar_cursos():
    token = request.form.get('token')  # o request.args.get si es GET
    cursos = obtener_cursos(token)

    if cursos is not None:
        return render_template('canvaslms2.html', cursos=cursos, token=token)
    else:
        return render_template('canvaslms2.html', error="No se pudo obtener los cursos")

@canvaslms.route('/canvas/recopilar_material/<curso_id>', methods=['POST'])
def recopilar_material_ruta(curso_id):
    token = request.form.get('token')
    carpeta_nombre = request.form.get('carpeta_nombre', curso_id)

    materiales = obtener_materiales_curso(token, curso_id)
    if not materiales:
        return "No se encontraron materiales para este curso", 404

    archivo_zip = recopilar_material(curso_id, materiales, carpeta_nombre)

    # 🧠 Aquí validamos que el ZIP exista

    ruta_completa = os.path.abspath(archivo_zip)
    print("Ruta del ZIP generada:", ruta_completa)

    if not os.path.exists(ruta_completa):
        return f"Archivo ZIP no encontrado en {ruta_completa}", 500

    return send_file(ruta_completa, as_attachment=True)