from flask_wtf import FlaskForm
from wtforms.fields import StringField,EmailField,SubmitField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Length,Regexp,Email,EqualTo,ValidationError
from ..models import User


class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[
                                            InputRequired(message='Nombre de usuario requerido'),
                                            Length(min=4,max=25,message='Ingrese un username valido'),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters,''numbers, dots or underscores')
    ])

    email = EmailField('Email',validators=[
                                           InputRequired('Email requerido'),
                                           Length(1,64),
                                           Email('Direccion de email invalido')

    ])

    password = PasswordField('Password',validators=[
                                                    InputRequired('Password requerido'),
                                                    EqualTo('password2',message='Las contraseñas deben coincidr')
    ])
    password2 = PasswordField('Confirm password',validators=[
                                                            InputRequired('Password requerido')])
    submit = SubmitField('Registrarse')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email ya esta registrado')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username ya esta en uso')



class LoginForm(FlaskForm):
    email = EmailField('Email',validators=[
                                           InputRequired(),
                                           Length(1,64),
                                           Email()

    ])
    password = PasswordField('Password',validators=[InputRequired()])
    remember_me = BooleanField('Mantenerme conectado')

    submit = SubmitField('Login')