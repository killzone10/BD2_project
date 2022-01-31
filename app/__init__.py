from turtle import back
from xmlrpc.client import Boolean
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os 
p = os.environ.get('SECRET_KEY')
app = Flask(__name__, template_folder='./templates')

# app.secret_key = '\xea\x1a\xb2\x8a\xefk\xd6V%\xf7\xb4\xe5\xa9\r=&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:linux123@localhost/products' ## postgres ://nazwa uzytkownima : haslo @ localhost/nazwa bazy danych
app.config['SECRET_KEY']=p
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view ='login'
login_manager.login_message_category = 'info'

from app import routes