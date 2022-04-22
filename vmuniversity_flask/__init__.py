from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY']='thisisfirstflaskapp'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database/vmuniversity.db'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database/vmuniversitycourses.db'

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
from vmuniversity_flask import VMUniversity

