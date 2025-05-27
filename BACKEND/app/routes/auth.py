# BACKEND/app/routes/auth.py

'''Configurando la autenticación'''
import random
import string
from flask import Blueprint, request, url_for, session, redirect
from app import oauth
import requests

# Función para generar un nonce aleatorio
def generate_nonce():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Configuración del Blueprint de autenticación
auth = Blueprint('auth', __name__)

# Ruta de login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Generar un nonce y guardarlo en la sesión
        session['nonce'] = generate_nonce()

        # Redirigir al usuario a Google para la autorización
        redirect_uri = url_for('auth.callback', _external=True)
        return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

    # Si es un GET, también generamos el nonce y redirigimos
    session['nonce'] = generate_nonce()
    return oauth.google.authorize_redirect(url_for('auth.callback', _external=True), nonce=session['nonce'])


# Ruta de callback de Google
@auth.route('/auth/callback')
def callback():
    # Obtener el token de Google
    token = oauth.google.authorize_access_token()

    # Recuperar el nonce de la sesión
    nonce = session.get('nonce')

    if not nonce:
        # Si no hay nonce en la sesión, redirigir al login u otra página
        return redirect(url_for('auth.login'))

    # Verificar el ID token de Google con el nonce
    user = oauth.google.parse_id_token(token, nonce=nonce)

    # Guardar el usuario y el token en la sesión
    session['user'] = user
    session['google_token'] = token  # Guardar el token de Google en la sesión

    # Redirigir al perfil u otra vista
    return redirect(url_for('perfil.profile'))


# Ruta de logout
@auth.route('/logout')
def logout():
    # Verificar y mostrar el contenido actual de la sesión (para depuración)
    print("Datos actuales de la sesión: ", session)

    # Obtener el token de Google desde la sesión
    google_token = session.get('google_token')
    if google_token:
        # Si hay un token, proceder a revocar el acceso
        revoke_url = f'https://oauth2.googleapis.com/revoke?token={google_token["access_token"]}'
        response = requests.post(revoke_url)

        # Si la revocación fue exitosa
        if response.status_code == 200:
            print("Token revocado correctamente")
            session.clear()  # Limpiar toda la sesión de Flask
        else:
            print("Error al revocar el token de Google: ", response.status_code)
            return "Error al revocar el token de Google.", 400
    else:
        print("No se encontró el token de Google en la sesión")

    # Verificar que la sesión ha sido limpiada completamente
    print("Sesión después de logout: ", session)

    # Redirigir a la página de inicio o login
    return redirect(url_for('carga_pd.pd_carga'))
