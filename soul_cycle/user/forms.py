from flask_wtf import Form
from wtforms import validators, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.fields import SubmitField

class LoginForm(Form):
    email = EmailField('Email', validators=[validators.Required()])
    password = PasswordField('Password', validators=[validators.Required()])
    submit = SubmitField('Submit')
