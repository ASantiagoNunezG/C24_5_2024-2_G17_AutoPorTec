# BACKEND/app/__init__.py
import os
from flask import Flask
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
load_dotenv()

# Importar blueprints solo dentro de create_app, después de que oauth esté configurado
from app.routes.ayuda import ayuda
from app.routes.canvaslms import canvaslms
from app.routes.routes import home_bp
from app.routes.pd_routes import carga_pd
from app.routes.perfil import perfil
from app.routes.portafolio_digital import portafolio_digital

# Inicializar OAuth globalmente
oauth = OAuth()

def create_app():
    app = Flask(__name__)

    # Configuraciones
    app.secret_key = "clave-super-secreta-de-auto-por-tec"


    # Configurar oauth con la app
    oauth.init_app(app)

    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        access_token_url='https://oauth2.googleapis.com/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v2/',
        userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo',
        client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/drive'},
        redirect_uri='http://localhost:5000/auth/callback'
    )

    # Ahora, importamos y registramos el blueprint de autenticación
    from app.routes.auth import auth
    app.register_blueprint(auth)

    # Registrar otros blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(carga_pd)
    app.register_blueprint(perfil)
    app.register_blueprint(ayuda)
    app.register_blueprint(canvaslms)
    app.register_blueprint(portafolio_digital)

    return app