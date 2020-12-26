from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Registro(FlaskForm):
    usuario = StringField('Usuario',
                        validators=[DataRequired(), Length(min=3,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Enviar')

class Login(FlaskForm):
    usuario = StringField('Usuario',
                        validators=[DataRequired(), Length(min=3,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')