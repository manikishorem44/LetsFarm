# Manikishore Medam, mm5224@drexel.edu
# CS 530: DUI , Final Project
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'
app.config['SECRET_KEY'] = 'b7f096adf032cf1891d49474c06a0009'
db = SQLAlchemy(app)
login = LoginManager(app)

from community import routes