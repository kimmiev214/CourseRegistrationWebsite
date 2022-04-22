from vmuniversity_flask import db
from datetime import datetime
#this creates the user database object
class User(db.Model):
    '''Users database class'''
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.username} : {self.email} : {self.date_created.strftime("%d/%m/%Y, %H:%M:%S")}'

class Course(db.Model):
    '''Courses database class'''
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60), unique=False, nullable=False)
    description=db.Column(db.String(250), unique=False, nullable=True)
    professor=db.Column(db.String(30), unique=False, nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.name} : {self.professor} : {self.date_created.strftime("%d/%m/%Y, %H:%M:%S")}'
