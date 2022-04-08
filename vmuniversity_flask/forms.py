#imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

'''Forms for Registering and Student Login'''
class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=12, max=30)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=12, max=20)])
    confirm_password= PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    create_account = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=12, max=20)])
    login = SubmitField(label='Sign in')