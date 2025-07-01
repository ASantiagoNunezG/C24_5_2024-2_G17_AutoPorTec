# BACKEND/app/services/estructura_portafolio_service.py
from app.services.google_drive_service import crear_carpeta_drive, listar_carpetas_drive


# Diccionario del Portafolio Digital con sus respectivas carpetas y subcarpetas
def estructura_portafolio_digital():
    estructura_portafolio_digital = {
        '1. Plan de Temas y Silabus': {},
        '2. Enlace a Canvas': {},
        '3. Material Teórico': {},
        '4. Guía de Laboratorio o Taller': {},
        '5. Planes de Clase': {
            'Teoría': {},
            'Laboratorio': {}
        },
        '6. Muestras de Prácticas Calificadas': {},
        '7. Muestras de Laboratorio, Talleres o Proyectos Calificados': {},
        '8. Evidencias de la Aplicación de Rúbricas PMD': {},
        '9. Material Complementario': {
            'Semana 01': {},
            'Semana 02': {},
            'Semana 03': {},
            'Semana 04': {},
            'Semana 05': {},
            'Semana 06': {},
            'Semana 07': {},
            'Semana 08': {},
            'Semana 09': {},
            'Semana 10': {},
            'Semana 11': {},
            'Semana 12': {},
            'Semana 13': {},
            'Semana 14': {},
            'Semana 15': {},
            'Semana 16': {}
        },
        '10. Informe de Fin de Curso': {}
    }
    return estructura_portafolio_digital


 # Se busca o crea una nueva carpeta = Portafolio Digital
def buscar_o_crear_carpeta(access_token, nombre_carpeta, parent_id):
    # Buscar si ya existe una carpeta con ese nombre en ese padre
    existentes = listar_carpetas_drive(access_token, parent_id)
    for carpeta in existentes:
        if carpeta['name'] == nombre_carpeta:
            return carpeta['id']

    # Si no existe, la creamos
    return crear_carpeta_drive(access_token, nombre_carpeta, parent_id)

def crear_estructura_con_lookup(access_token, parent_id, estructura, ids=None, ruta_anterior=""):
    if ids is None:
        ids = {}

    for nombre, subestructura in estructura.items():
        carpeta_id = buscar_o_crear_carpeta(access_token, nombre, parent_id)

        # RUTA basada en nombres legibles, no en IDs
        ruta = f"{nombre}" if not ruta_anterior else f"{ruta_anterior}/{nombre}"
        ids[ruta] = carpeta_id

        if subestructura:
            crear_estructura_con_lookup(access_token, carpeta_id, subestructura, ids, ruta)

    return ids

def obtener_o_crear_carpeta_profesor(access_token, carpeta_padre_id, profesor_nombre):
    existentes = listar_carpetas_drive(access_token, carpeta_padre_id)
    for carpeta in existentes:
        if carpeta['name'] == profesor_nombre:
            return carpeta['id']
    return crear_carpeta_drive(access_token, profesor_nombre, carpeta_padre_id)

def crear_o_obtener_carpeta_de_ruta(access_token, ruta, ids, carpeta_raiz_id):
    partes = ruta.split('/')
    parent_id = carpeta_raiz_id
    for parte in partes:
        key = f"{parent_id}/{parte}"
        if key not in ids:
            parent_id = buscar_o_crear_carpeta(access_token, parte, parent_id)
            ids[key] = parent_id
        else:
            parent_id = ids[key]
    return parent_id