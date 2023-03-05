from . import notices
from flask import render_template,redirect,url_for,request,send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required,current_user

from .forms import NoticeForm
from .. import db
from ..funciones import allowed_file,getFolder
from ..models import Post
import os

@notices.route('/createNotice',methods=['GET','POST'])
@login_required
def createNotice():
    formPost = NoticeForm()

    if formPost.validate_on_submit():
        titulo = formPost.title.data
        contenido = formPost.body.data
        autor = current_user._get_current_object()
        #comprueba si la peticion contiene la parte del fichero
        if "img_not" not in request.files:
            return "El formulario no tiene parte del archivo"
        f = request.files["img_not"]
        if f.filename == f.filename == "":
            return "Ningun archivo seleccionado"
        if f and allowed_file(f.filename):
            image_name = secure_filename(f.filename)
            f.save(os.path.join(getFolder(),image_name))
        post = Post(title=titulo, body= contenido, author=autor,img=image_name)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('form_notice.html',form=formPost)

@notices.route("/get_imgNoti/<filename>")
def get_imgNoti(filename):
    return send_from_directory(getFolder(),filename)

@notices.route('/seeNotices')
def seeNotices():
    cantidad=5
    page = request.args.get('page',type=int)

    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=cantidad,error_out=False)
    posts = pagination.items
    return render_template('notices.html', posts=posts,pagination=pagination)

@notices.route('/editNotice/<int:id>',methods=['GET','POST'])
@login_required
def editNotice(id):
    post = Post.query.get_or_404(id)
    form = NoticeForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        if "img_not" not in request.files:
            return "El formulario no tiene parte del archivo"
        f = request.files["img_not"]
        if f and allowed_file(f.filename):
            image_name = secure_filename(f.filename)
            f.save(os.path.join(getFolder(),image_name))
            post.img = image_name
        db.session.add(post)
        db.session.commit()
        print('El post se ha actualizado')
        return redirect(url_for('notices.seeNotices',id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('form_notice.html',form=form)

@notices.route('/deleteNotice/<id>')
@login_required
def deleteNotice(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('notices.seeNotices'))