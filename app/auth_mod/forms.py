# Import Form and Recaptcha
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form Elements
from wtforms import StringField, PasswordField # BooleanField

# Import Form validation
from wtforms.validators import InputRequired, Email, EqualTo

# Define Login Form
class LoginForm(FlaskForm):
	email	 = StringField('Email', [Email(), InputRequired(message='Seems you forgot your email. Strange.')])
	password = PasswordField('Password',   [InputRequired(message='Dont foget the password.')])


