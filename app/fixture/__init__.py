from flask import Blueprint

fixture = Blueprint('fixture',__name__,template_folder='templates')

from . import views