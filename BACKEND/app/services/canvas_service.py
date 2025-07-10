# BACKEND/app/services/canvas_service.py
import requests
from dotenv import load_dotenv
from flask import session
import os

load_dotenv()
BASE_CANVAS_URL = os.getenv('TECSUP_CANVAS_URL') # Modo TECSUP - docentes
#BASE_CANVAS_URL = os.getenv('BASE_CANVAS_URL') # Modo desarrollo
def obtener_cursos(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "include[]": "course_image"
    }
    url = f"{BASE_CANVAS_URL}/courses"
    response = requests.get(url, headers=headers, params = params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def obtener_materiales_curso(token, curso_id):

    archivos = []

    url = f"{BASE_CANVAS_URL}/courses/{curso_id}/files"
    headers = {"Authorization": f"Bearer {token}"}

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            archivos.extend(response.json())
            # Paginación
            url = response.links.get('next', {}).get('url')
        else:
            raise Exception(f"Error al obtener archivos: {response.status_code}, {response.text}")

    return archivos

def quitar_token_service():

    canvas_token = session.get('canvas_token')

    #Verificamos si el token de Canvas LMS existe
    if canvas_token:
        session.pop('canvas_token', None)
        return "Token de Canvas LMS eliminado correctamente"
    else:
        return "No se ha encontrado ningún token de Canvas LMS"

def obtener_material_por_modulo(token, curso_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 1. Obtener todos los módulos
    url_modulos = f"{BASE_CANVAS_URL}/courses/{curso_id}/modules"
    resp_modulos = requests.get(url_modulos, headers=headers)

    if resp_modulos.status_code != 200:
        raise Exception(f"Error al obtener módulos: {resp_modulos.status_code}, {resp_modulos.text}")

    modulos = resp_modulos.json()
    archivos_por_modulo = {}

    # 2. Iterar sobre los módulos
    for modulo in modulos:
        nombre_modulo = modulo["name"]
        url_items = f"{BASE_CANVAS_URL}/courses/{curso_id}/modules/{modulo['id']}/items"

        resp_items = requests.get(url_items, headers=headers)
        if resp_items.status_code != 200:
            continue  # saltar módulo si falla

        items = resp_items.json()

        # 3. Filtrar los archivos
        for item in items:
            if item["type"] == "File":
                nombre_archivo = item["title"]
                if nombre_modulo not in archivos_por_modulo:
                    archivos_por_modulo[nombre_modulo] = []
                archivos_por_modulo[nombre_modulo].append(nombre_archivo)

    return archivos_por_modulo
