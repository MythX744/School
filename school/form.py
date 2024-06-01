from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TextAreaField, RadioField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField(label="Email")
    password = PasswordField(label="Password")
    submit = SubmitField(label="Submit")


class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description')
    date = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Save Event')
