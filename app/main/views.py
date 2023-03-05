from . import main

from flask import render_template

from ..models import Post,Fixture,Blog

@main.route('/')
@main.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).limit(5).all()
    ultimoPartido = Fixture.query.order_by((Fixture.fecha_hora).asc()).first()
    partidos = Fixture.query.order_by((Fixture.fecha_hora).asc()).limit(3).all()
    blogs = Blog.query.order_by(Blog.timestamp.desc()).limit(2).all()

    return render_template('index.html', posts=posts,partido=ultimoPartido,partidos=partidos,blogs=blogs)

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
