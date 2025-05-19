from flask import session

import requests
import json

def upload_to_drive(access_token, file_stream, file_name, folder_id=None):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    metadata = {
        "name": file_name,
        "mimeType": "application/zip"
    }
    # Si se proporciona un ID de carpeta, lo agregamos como padre
    if folder_id:
        metadata['parents'] = [folder_id]

    multipart_boundary = "foo_bar_baz"

    # Metadata en JSON
    metadata_json = json.dumps(metadata)

    # Construir multipart body manualmente
    multipart_data = (
                         f'--{multipart_boundary}\r\n'
                         f'Content-Type: application/json; charset=UTF-8\r\n\r\n'
                         f'{metadata_json}\r\n'
                         f'--{multipart_boundary}\r\n'
                         f'Content-Type: application/zip\r\n\r\n'
                     ).encode('utf-8') + file_stream.read() + f'\r\n--{multipart_boundary}--'.encode('utf-8')

    headers["Content-Type"] = f"multipart/related; boundary={multipart_boundary}"

    upload_url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
    response = requests.post(upload_url, headers=headers, data=multipart_data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error al subir archivo:", response.text)
        return None
