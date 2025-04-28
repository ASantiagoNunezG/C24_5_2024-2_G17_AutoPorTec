# BACKEND/app/services/canvas_service.py
import requests

BASE_CANVAS_URL = "https://canvas.instructure.com/api/v1"

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