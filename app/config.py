import os

class Config():
    SECRET_KEY = "My_secret_key"
    FLASKY_ADMIN = "oalxo06@gmail.com"

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql://root:Al3x0rt1z@localhost/ddbbclubPrueba"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.abspath("./app/uploads/")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "oalxo06@gmail.com"
    MAIL_PASSWORD = "pjdjklrmfbxukiid"


config = {
    'development':DevelopmentConfig
}





