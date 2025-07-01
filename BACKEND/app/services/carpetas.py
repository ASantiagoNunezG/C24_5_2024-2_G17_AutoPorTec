# BACKEND/app/services/carpetas.py

from flask import session

from app.services.estructura_portafolio_service import estructura_portafolio_digital

diccionario_carpetas_portafolio = {i + 1: nombre for i, nombre in enumerate(estructura_portafolio_digital().keys())}

# Organización de los archivos en las carpetas
def obtener_carpeta_profesor(user):
    nombres = user.get("given_name", "").split()
    apellidos = user.get("family_name", "").split()

    if not nombres or not apellidos:
        return "SIN_IDENTIFICAR"

    inicial = nombres[0][0]  # Primera letra del primer nombre
    primer_apellido = apellidos[0]

    return f"{inicial.upper()}{primer_apellido.upper()}"  # Ej: ANUNEZ

# Función de Clasificación
def switch_clasificacion_archivo(nombre_archivo):

    nombre_archivo = nombre_archivo.upper()
    user = session.get("user", {})
    carpeta_profesor = obtener_carpeta_profesor(user)

    match True:
        case _ if nombre_archivo.startswith(("PT_", "S_")) and nombre_archivo.endswith((".DOCX", ".XLSX")):
            return diccionario_carpetas_portafolio[1]  # Plan de Temas y Silabus

        case _ if "ENLACE DEL CURSO" in nombre_archivo and nombre_archivo.endswith(".TXT"):
            return diccionario_carpetas_portafolio[2]  # Enlace a Canvas

        case _ if nombre_archivo.startswith("PPT-S") and nombre_archivo.endswith(("PPTX",".PDF")):
            return f"{diccionario_carpetas_portafolio[3]}/{carpeta_profesor}" # PPT-S01-AAVALOS-2024-01 <-> PPT-S[01-16]-[INICIAL DEL NOMBRE DEL USUARIO][APELLIDO DEL USUARIO]-[SEMESTRE]

        case _ if nombre_archivo.startswith(("GLAB", "GTAL", "PCAL")) and nombre_archivo.endswith((".DOCX", ".PDF")):
            return f"{diccionario_carpetas_portafolio[4]}/{carpeta_profesor}"

        case _ if nombre_archivo.endswith(".DOCX") and nombre_archivo.startswith(("PC", "PLAN", "PLAN_LAB")):
            if "PLAN_LAB" in nombre_archivo:
                subcarpeta = "Laboratorio"
            elif "PLAN" in nombre_archivo:
                subcarpeta = "Teoría"
            else:
                subcarpeta = ""  # PC va directo a Planes de Clase

            if subcarpeta:
                return f"{diccionario_carpetas_portafolio[5]}/{subcarpeta}/{carpeta_profesor}"
            else:
                return f"{diccionario_carpetas_portafolio[5]}/{carpeta_profesor}"

        case _ if nombre_archivo.startswith("PRACT"): # PRACT-01-AAVALOS-2024-01
            return f"{diccionario_carpetas_portafolio[6]}/{carpeta_profesor}"

        case _ if nombre_archivo.startswith(("LAB", "TALL", "PROY")): # LAB-01-AAVALOS-2024-01
            return f"{diccionario_carpetas_portafolio[7]}/{carpeta_profesor}"

        case _ if "PMD" in nombre_archivo or nombre_archivo.startswith(("ACTIVIDAD", "RÚBRICA")): # ACTIVIDAD-PMD-AAVALOS-2024-01 | RÚBRICA-PMD-AAVALOS-2024-01
            return f"{diccionario_carpetas_portafolio[8]}/{carpeta_profesor}"

        case _ if nombre_archivo.endswith((".MP4",".MP3")):
            nombre_modulo = "Semana 01"
            return f"{diccionario_carpetas_portafolio[9]}/{carpeta_profesor}/{nombre_modulo}"

        case _ if nombre_archivo.startswith("CORREO DE TECSUP") and nombre_archivo.endswith(".PDF"): #
            return f"{diccionario_carpetas_portafolio[10]}/{carpeta_profesor}"

        case _:
            return f"{diccionario_carpetas_portafolio[9]}/{carpeta_profesor}"


