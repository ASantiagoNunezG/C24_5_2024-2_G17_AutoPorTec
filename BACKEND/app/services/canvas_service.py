# BACKEND/app/services/canvas_service.py
import requests
from dotenv import load_dotenv
from flask import session
import os

load_dotenv()
#BASE_CANVAS_URL = os.getenv('TECSUP_CANVAS_URL')
BASE_CANVAS_URL = os.getenv('BASE_CANVAS_URL')
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
    if(canvas_token):
        session.pop('canvas_token', None)
        return "Token de Canvas LMS eliminado correctamente"
    else:
        return "No se ha encontrado ningún token de Canvas LMS"