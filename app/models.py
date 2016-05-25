from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))


    def get_user_id(self):
        return self.user_id    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)     

class Author(db.Model):
    __tablename__ = 'authors'
    author_id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index =True, unique = True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
