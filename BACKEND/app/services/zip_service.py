import io
import zipfile
import requests

def crear_zip_en_memoria(materiales):
    # Crea un buffer en memoria donde guardar el ZIP
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for archivo in materiales:
            nombre = archivo['display_name']
            url = archivo['url']

            # Descarga archivo (contenido en bytes)
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                contenido = respuesta.content
                # Agrega archivo al ZIP directamente desde memoria
                zipf.writestr(nombre, contenido)
            else:
                print(f"Error al descargar {nombre}")

    # Mover el cursor al inicio para lectura
    buffer.seek(0)
    return buffer

