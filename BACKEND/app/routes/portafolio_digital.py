# BACKEND/app/routes/portafolio_digital.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.estructura_portafolio_service import generar_portafolio_digital

portafolio_digital = Blueprint('portafoliod', __name__)

@portafolio_digital.get('/portafoliod')
def portafolio():
    return render_template('portafolio_digital.html')

@portafolio_digital.post('/generar_pd')  # <-- agrega la barra al inicio
def generar_pd():
    # Obtener nombre del formulario correctamente
    nombre_portafolio = request.form.get('nombre_portafolio')

    if not nombre_portafolio:
        flash("Por favor ingresa un nombre para el portafolio.", "error")
        return redirect(url_for('portafoliod.portafolio'))

    ruta = generar_portafolio_digital(nombre_portafolio)

    flash(f"Portafolio generado correctamente en: {ruta}", "success")
    return redirect(url_for('portafoliod.portafolio'))