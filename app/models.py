from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import check_password_hash,generate_password_hash
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from flask import current_app
from datetime import datetime

from sqlalchemy.orm import relationship

from . import db,login_manager

ALLOWED_EXTENSIONS = set(['png','jpg','jpge','gif'])

# ---------------------------------------------------------------------
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE = 0x04
    MODERATE = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False,index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE | Permission.MODERATE,False),
            'Administrator':(0xff,False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean,default=False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    posts = db.relationship('Post',backref='author', lazy='dynamic')
    blogs = db.relationship('Blog',backref='author', lazy='dynamic')

    # Password verification --------------------------------------------
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash= generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    # Email confirmation -----------------------------------------------
    def generate_confirmation_token(self, email):
        s =URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm':email}, salt='email-confirm')

    def confirm(self, token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='email-confirm',max_age=3600)
        except SignatureExpired:
            return False
        if data.get('confirm') != self.email:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    # Asignar rol default y admin  -----------------------------------------
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # Metodos para roles ---------------------------------------------------
    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    #Capturar tiempo-------------------------------------------------------------------------
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    #Generar usuarios ramdom-fake --------------------------------------------
    # @staticmethod
    # def generate_fake(count=30):
    #     from sqlalchemy.exc import IntegrityError
    #     from random import seed
    #     import forgery_py

    #     seed()
    #     for i in range(count):
    #         u = User(email=forgery_py.internet.email_address(),
    #                  username=forgery_py.internet.user_name(True),
    #                  password=forgery_py.lorem_ipsum.word(),
    #                  confirmed=True,
    #                  name=forgery_py.name.full_name(),
    #                  location=forgery_py.address.city(),
    #                  about_me=forgery_py.lorem_ipsum.sentence(),
    #                  member_since=forgery_py.date.date(True))
    #         db.session.add(u)
    #         try:
    #             db.session.commit()
    #         except IntegrityError:
    #             db.session.rollback()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    img= db.Column(db.String(100))

    # @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0,user_count-1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1,3)),timestamp=forgery_py.date.date(True),author=u)
            db.session.add(p)
            db.session.commit()

    # @staticmethod
    def generate_fake_one(author_id,count):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            p = Post(title=forgery_py.lorem_ipsum.sentence(),body=forgery_py.lorem_ipsum.sentences(randint(10,20)),timestamp=forgery_py.date.date(True),author=author_id)
            db.session.add(p)
            db.session.commit()

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

# --------------------------------------------------------------------

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(100))
    logo = db.Column(db.String(100))

    def allowed_file(filename):
        return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS

class Fixture(db.Model):
    __tablename__ = 'fixture'
    id = db.Column(db.Integer, primary_key=True)
    Local_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    Visita_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    Local = relationship("Team",foreign_keys=[Local_id])
    Visita = relationship("Team",foreign_keys=[Visita_id])

    fecha_hora = db.Column(db.DateTime(timezone=True))
    lugar = db.Column(db.Text())
    resLocal = db.Column(db.String(50))
    resVisita = db.Column(db.String(50))
    golLocal = db.Column(db.Integer)
    golVisita = db.Column(db.Integer)

    estado = db.Column(db.String(50))

class Positions(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(100))
    p_ganado = db.Column(db.Integer)
    p_empatado = db.Column(db.Integer)
    p_perdido = db.Column(db.Integer)
    p_jugados = db.Column(db.Integer)
    puntos = db.Column(db.Integer)
    gf = db.Column(db.Integer)
    ge = db.Column(db.Integer)
    df = db.Column(db.Integer)

    id_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    tablaPosicion = relationship("Team",foreign_keys=[id_team])

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    img_blog= db.Column(db.String(100))

    # @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0,user_count-1)).first()
            p = Blog(body=forgery_py.lorem_ipsum.sentences(randint(1,3)),timestamp=forgery_py.date.date(True),author=u)
            db.session.add(p)
            db.session.commit()

    # @staticmethod
    def generate_fake_one(author_id,count):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            p = Blog(title=forgery_py.lorem_ipsum.sentence(),body=forgery_py.lorem_ipsum.sentences(randint(10,20)),timestamp=forgery_py.date.date(True),author=author_id)
            db.session.add(p)
            db.session.commit()

