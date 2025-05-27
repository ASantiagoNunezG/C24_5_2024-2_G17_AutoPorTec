import os

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

