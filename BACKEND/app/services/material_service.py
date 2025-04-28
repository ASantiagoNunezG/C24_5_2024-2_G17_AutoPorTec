# BACKEND/app/services/material_service.py
import os
import zipfile
import requests

def crear_carpeta(carpeta_nombre):
    ruta_carpeta = f"./materiales/{carpeta_nombre}/"
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    return ruta_carpeta

def descargar_archivo(url, carpeta_destino, nombre_archivo):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(carpeta_destino, nombre_archivo), 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Error al descargar el archivo desde {url}")

def crear_zip(carpeta_origen, archivo_destino):
    with zipfile.ZipFile(archivo_destino, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(carpeta_origen):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

def recopilar_material(curso_id, materiales, carpeta_nombre):
    carpeta_destino = crear_carpeta(carpeta_nombre)

    for material in materiales:
        archivo_url = material.get('url') or material.get('url_private_download') # Obtener URL del material
        nombre_archivo = material.get('filename') or material.get('display_name') or material.get('name')  # Nombre del archivo
        try:
            descargar_archivo(archivo_url, carpeta_destino, nombre_archivo)
        except Exception as e:
            return f"Error al descargar el archivo {nombre_archivo}: {e}"

    archivo_zip = f"{carpeta_destino}.zip"
    crear_zip(carpeta_destino, archivo_zip)

    return archivo_zip
