from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    number = StringField('Number',  validators=[InputRequired()])
    address = TextAreaField('Address', validators=[InputRequired()])
    submit = SubmitField('Submit Information')