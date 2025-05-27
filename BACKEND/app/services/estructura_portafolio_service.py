# BACKEND/app/services/estructura_portafolio_service.py
import os

from app.services.google_drive_service import crear_carpeta_drive


def generar_portafolio_digital(nombre_portafolio):
    lista_carpetas_portafolio = [
        'Plan de Temas y Silabus',
        'Enlace a Canvas',
        'Material Teórico',
        'Guía de Laboratorio o Taller',
        'Planes de Clase',
        'Muestras de Prácticas Calificadas',
        'Muestras de Laboratorio, Talleres o Proyectos Calificados',
        'Evidencias de la Aplicación de Rúbricas PMD',
        'Material Complementario',
        'Informe de Fin de Curso',
    ]

    # Ruta donde se creará el portafolio digital (ajusta según tu sistema)
    ruta_base = f"C:/Users/USUARIO/Downloads/{nombre_portafolio}/"
    os.makedirs(ruta_base, exist_ok=True)

    # Crear carpetas numeradas
    for idx, nombre in enumerate(lista_carpetas_portafolio, start=1):
        nombre_carpeta = f"{idx}. {nombre}"
        ruta_carpeta = os.path.join(ruta_base, nombre_carpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)

    print(f"Portafolio '{nombre_portafolio}' generado exitosamente en: {ruta_base}")
    return ruta_base  # útil si luego quieres mostrar ruta en la interfaz


def clasificar_archivo(nombre_archivo):
    """
    Clasifica el archivo según el prefijo en el nombre para determinar
    en qué carpeta debe ir dentro del portafolio.

    Retorna el nombre de la carpeta donde debe ir el archivo.
    """
    nombre_archivo = nombre_archivo.upper()  # Ignorar mayúsculas/minúsculas

    if nombre_archivo.startswith("PC"):

        # Planes de Clase -> subcarpetas Teoría o Taller
        
        if "TEORIA" in nombre_archivo:
            return "5. Planes de Clase/Teoría"
        elif "TALLER" in nombre_archivo:
            return "5. Planes de Clase/Taller"
        else:
            return "5. Planes de Clase"

    elif nombre_archivo.startswith("PPT"):
        return "3. Material Teórico"

    elif nombre_archivo.startswith(("GLAB", "GTAL", "PCAL")):
        return "4. Guía de Laboratorio o Taller"

    elif nombre_archivo.startswith("ENLACE"):
        return "2. Enlace a Canvas"


    else:
        # Si no encaja en ninguna categoría, lo dejamos en Material No Identificado
        return "11. Material No Identificado"

def crear_estructura_portafolio_drive(access_token, carpeta_principal_id):
    lista_carpetas_portafolio = [
        'Plan de Temas y Silabus',
        'Enlace a Canvas',
        'Material Teórico',
        'Guía de Laboratorio o Taller',
        'Planes de Clase',
        'Muestras de Prácticas Calificadas',
        'Muestras de Laboratorio, Talleres o Proyectos Calificados',
        'Evidencias de la Aplicación de Rúbricas PMD',
        'Material Complementario',
        'Informe de Fin de Curso',
        'Material No Identificado'  # Cambio aquí
    ]

    carpetas_ids = {}

    for idx, nombre in enumerate(lista_carpetas_portafolio, start=1):
        nombre_carpeta = f"{idx}. {nombre}"  # Numeración añadida
        carpeta_id = crear_carpeta_drive(access_token, nombre_carpeta, parent_id=carpeta_principal_id)
        if carpeta_id:
            carpetas_ids[nombre_carpeta] = carpeta_id

            # Manejo subcarpetas para "Planes de Clase"
            if nombre == "Planes de Clase":
                sub_teoria_id = crear_carpeta_drive(access_token, 'Teoría', parent_id=carpeta_id)
                sub_taller_id = crear_carpeta_drive(access_token, 'Taller', parent_id=carpeta_id)
                carpetas_ids[f"{idx}. Planes de Clase/Teoría"] = sub_teoria_id
                carpetas_ids[f"{idx}. Planes de Clase/Taller"] = sub_taller_id
        else:
            print(f"Error creando carpeta: {nombre_carpeta}")

    return carpetas_ids
