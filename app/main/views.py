from . import main

from flask import render_template

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@main.route('/academia')
def academia():
    return render_template('academia.html')

@main.route('/contacto')
def contacto():
    return render_template('contacto.html')

@main.route('/tienda')
def tienda():
    return render_template('tienda.html')
