from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms.fields import SubmitField,StringField
from wtforms.validators import InputRequired

class TeamForm(FlaskForm):
    team = StringField('Equipo',validators=[InputRequired()])
    img_logo = FileField('Logo',validators=[FileAllowed(['jpg','png'],'Solo se permiten imagenes')]) 
    submit = SubmitField('Guardar')
