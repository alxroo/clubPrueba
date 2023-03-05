import os

class Config():
    SECRET_KEY = ""
    FLASKY_ADMIN = "

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.abspath("./app/uploads/")

    MAIL_SERVER = ""
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""


config = {
    'development':DevelopmentConfig
}





