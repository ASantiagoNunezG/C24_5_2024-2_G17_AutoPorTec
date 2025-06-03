# BACKEND/app/services/google_drive_service.py

import requests
import json

def subir_archivo_a_drive(access_token, nombre, contenido, mime_type, folder_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    if isinstance(nombre, bytes):
        nombre = nombre.decode('utf-8')  # Decodifica si fuera necesario

    metadata = {
        'name': nombre,
        'parents': [folder_id]
    }

    files = {
        'metadata': (
            'metadata',
            json.dumps(metadata, ensure_ascii=False).encode('utf-8'),
            'application/json; charset=UTF-8'
        ),
        'file': ('file', contenido, mime_type)
    }

    response = requests.post(
        'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
        headers=headers,
        files=files
    )

    return response.json() if response.status_code == 200 else None

def crear_carpeta_drive(access_token, nombre_carpeta, parent_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    metadata = {
        "name": nombre_carpeta,
        "mimeType": "application/vnd.google-apps.folder"
    }

    if parent_id:
        metadata["parents"] = [parent_id]

    response = requests.post(
        "https://www.googleapis.com/drive/v3/files",
        headers=headers,
        data=json.dumps(metadata)
    )

    if response.status_code == 200:
        return response.json()["id"]
    else:
        print("Error creando carpeta:", response.content)
        return None
'''
def listar_archivos(folder_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": f"'{folder_id}' in parents and trashed=false",
        "fields": "files(id, name, mimeType, webViewLink)"
    }
    response = requests.get("https://www.googleapis.com/drive/v3/files", headers=headers, params=params)

    if response.ok:
        return response.json()["files"]
    else:
        print("Error al listar archivos:", response.text)
        return []
'''