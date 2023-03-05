from . import blogs
from flask import Flask,render_template,request,redirect,url_for,send_from_directory
from flask_login import current_user,login_required
from werkzeug.utils import secure_filename
import os

from .forms import BlogForm
from .. import db
from ..funciones import allowed_file,getFolder
from ..models import Blog


@blogs.route('/createBlog',methods=['GET','POST'])
def createBlog():
    formBlog = BlogForm() 
    # return render_template('createblog.html',form=formBlog)
    if formBlog.validate_on_submit():
        titulo = formBlog.title.data
        contenido = formBlog.body.data
        autor = current_user._get_current_object()
        #comprueba si la peticion contiene la parte del fichero
        if "img_blog" not in request.files:
            return "El formulario no tiene parte del archivo"
        f = request.files["img_blog"]
        if f.filename == f.filename == "":
            return "Ningun archivo seleccionado"
        if f and allowed_file(f.filename):
            image_name = secure_filename(f.filename)
            f.save(os.path.join(getFolder(),image_name))
        post = Blog(title=titulo, body= contenido, author=autor,img_blog=image_name)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('createblog.html',form=formBlog)

@blogs.route("/get_imgBlog/<filename>")
def get_imgBlog(filename):
    return send_from_directory(getFolder(),filename)

@blogs.route('/see_blog')
def see_blog():
    cantidad=5
    page = request.args.get('page',type=int)

    pagination = Blog.query.order_by(Blog.timestamp.desc()).paginate(page=page, per_page=cantidad,error_out=False)
    items = pagination.items
    return render_template('blog.html', items=items,pagination=pagination)

@blogs.route('/editBlog/<int:id>',methods=['GET','POST'])
@login_required
def editBlog(id):
    blogitem = Blog.query.get_or_404(id)
    form = BlogForm()
    if form.validate_on_submit():
        blogitem.title = form.title.data
        blogitem.body = form.body.data
        if "img_blog" not in request.files:
            return "El formulario no tiene parte del archivo"
        f = request.files["img_blog"]
        if f and allowed_file(f.filename):
            image_name = secure_filename(f.filename)
            f.save(os.path.join(getFolder(),image_name))
            blogitem.img = image_name
        db.session.add(blogitem)
        db.session.commit()
        print('El blog se ha actualizado')
        return redirect(url_for('blogs.see_blog',id=blogitem.id))
    form.title.data = blogitem.title
    form.body.data = blogitem.body
    return render_template('createblog.html',form=form)


@blogs.route('/deleteBlog/<id>')
@login_required
def deleteBlog(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('blogs.see_blog'))

