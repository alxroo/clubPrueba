from . import auth
from flask import render_template,request,redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user

from app import db
from app.models import User
from .forms import RegisterForm,LoginForm
from .email import send_email

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('email/unconfirmed.html')

@auth.route('/login',methods=['GET','POST'])
def login():
    loginForm = LoginForm()
    if request.method == 'POST' and loginForm.validate_on_submit():
        email = loginForm.email.data
        password = loginForm.password.data
        remember_me = loginForm.remember_me.data

        userlogin = User.query.filter_by(email=email).first()

        if userlogin is not None and userlogin.verify_password(password):
            login_user(userlogin,remember_me)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Usuario o password invalido')
       
    return render_template('login.html',form = loginForm)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    registerForm = RegisterForm()
    if request.method == 'POST' and registerForm.validate_on_submit():
        username = registerForm.username.data
        email = registerForm.email.data
        password = registerForm.password.data

        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        token = new_user.generate_confirmation_token(new_user.email)
        link = url_for('auth.confirm', token=token, _external=True)
        send_email('Confirm your Account',
                    sender='oalxo06@gamil.com',
                    recipients=[new_user.email],
                    text_body=render_template('email/confirm.txt',user=new_user, link=link),
                    html_body=render_template('email/confirm.html',user=new_user,link=link))

        flash('Se le ha enviado un correo electronico de confirmacion de cuenta')
        return redirect(url_for('auth.login'))
    return render_template('signup.html',form = registerForm)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks')
    else:
        flash('The confirmation links is invalid or has expired')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token(current_user.email)
    link = url_for('auth.confirm',token=token, _external=True)

    send_email('Confirm Your Account',
             sender='oalxo06@gmail.com',
             recipients=[current_user.email],
             text_body=render_template('email/confirm.txt',user=current_user, link=link),
             html_body=render_template('email/confirm.html',user=current_user, link=link),)

    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesion')
    return redirect(url_for('main.index'))

@auth.route('/options')
@login_required
def options():
    return render_template('options.html')













