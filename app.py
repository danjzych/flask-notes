import os

from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "secret"

connect_db(app)


@app.get('/')
def homepage_redirect():

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def handle_register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        return redirect(f"/users/{username}")

    else:
        return render_template('user_form.html', form=form, title="register")


@app.route('/login', methods=['GET', 'POST'])
def handle_login():
    """Render login form or handle login"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("user_form.html", form=form, title="login")


