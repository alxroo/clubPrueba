from flask import Blueprint

blogs = Blueprint('blogs',__name__,template_folder='templates')

from . import views