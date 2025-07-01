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


def listar_carpetas_drive(access_token, parent_id):
    url = "https://www.googleapis.com/drive/v3/files"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    query = (
        f"'{parent_id}' in parents and "
        f"mimeType = 'application/vnd.google-apps.folder' and "
        f"trashed = false"
    )

    params = {
        "q": query,
        "fields": "files(id, name)",
        "pageSize": 1000
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("files", [])
    else:
        print("Error al listar carpetas:", response.text)
        return []

def archivo_existe_en_drive(access_token, folder_id, nombre_archivo):
    url = "https://www.googleapis.com/drive/v3/files"
    headers = {"Authorization": f"Bearer {access_token}"}
    query = (
        f"'{folder_id}' in parents and "
        f"name = '{nombre_archivo}' and "
        f"trashed = false"
    )
    params = {
        "q": query,
        "fields": "files(id, name)",
        "pageSize": 1
    }
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 200:
        return len(resp.json().get("files", [])) > 0
    return False
