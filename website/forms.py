from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, EqualTo

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), validators.EqualTo('new_password', message='Passwords not match. Please try again.')])
