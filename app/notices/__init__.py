from flask import Blueprint

notices = Blueprint('notices',__name__,template_folder='templates')

from . import views