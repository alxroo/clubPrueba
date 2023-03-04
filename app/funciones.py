from .config import DevelopmentConfig

ALLOWED_EXTENSIONS = set(['png','jpg','jpge','gif'])

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS

def getFolder():
    folder = DevelopmentConfig().UPLOAD_FOLDER
    return folder