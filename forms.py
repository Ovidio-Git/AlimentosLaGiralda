from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import PasswordField, TextField, SubmitField
from wtforms.validators import InputRequired     #validores

# crea una clase que extiende de Flaskform y se llama Login()
class Search(FlaskForm):     # 
    
    name = TextField('name')
    btn = SubmitField('Buscar')