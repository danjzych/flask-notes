from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    """Form for registering a user in notes app."""

    username = StringField('Username', validators=[InputRequired(),
                                                   Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                   Length(min=10)])
    email = EmailField('Email', validators=[InputRequired()]) #Email()]
    first_name = StringField('First Name', validators=[InputRequired(),
                                                       Length(min=1, max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(),
                                                       Length(min=1, max=30)])

class LoginForm(FlaskForm):
    """Form for registering a user in notes app."""

    username = StringField('Username', validators=[InputRequired(),
                                                   Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                   Length(min=10)])


class CSRFProtectForm(FlaskForm):
    """Form to handle CSRF protection for logouts."""


class AddNoteForm(FlaskForm):
    """Form for adding a note in the note app."""

    title = StringField('Title', validators=[InputRequired(),
                                                   Length(min=1, max=100)])
    content = TextAreaField('Note', validators=[InputRequired()])