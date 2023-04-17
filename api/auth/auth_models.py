from flask_login import UserMixin
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from app import create_app, sql_db

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
# sql_db = SQLAlchemy(app)

app = create_app()

class User(UserMixin, sql_db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = sql_db.Column(sql_db.Integer, primary_key=True)
    username = sql_db.Column(sql_db.String(80), unique=True, nullable=False)
    password = sql_db.Column(sql_db.String(300), nullable=False, unique=True)
    # email = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    # pwd = sql_db.Column(sql_db.String(300), nullable=False, unique=True)

    def __init__(self, username, password):
        self.username = username
        # self.email =
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class UserProfile(sql_db.Model):
    __tablename__ = 'userprofile'
    __table_args__ = {'extend_existing': True}
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    full_name = sql_db.Column(sql_db.String(120))
    email = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    phone = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    # biography = sql_db.Column(sql_db.String(120), unique=True, nullable=False)

    def __init__(self, full_name, email, phone, bio=""):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.bio = bio


with app.app_context():
    sql_db.create_all()

    if not User.query.filter_by(username='user1').first():
        sql_db.session.add(User('user1', 'user1234'))
        sql_db.session.commit()

    users = User.query.all()
    print(users)