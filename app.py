import os

from flask import Flask, request, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "secret"

connect_db(app)


@app.get('/')
def homepage_redirect():
    """Redirect to register page."""

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def handle_register():
    """Handle the registration form for new user creation."""

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
        # global constant for AUTH_KEY="username"
        session["username"] = new_user.username
        flash('User registered succesfully!')
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
            flash('Your username our password is incorrect!')
            form.username.errors = ["Bad name/password"]

    return render_template("user_form.html", form=form, title="login")


@app.get('/users/<username>')
def show_user_info(username):
    """Show user profile for logged in users."""
    # fail fast, check if user NOT in session first, then rest not in conditional

    form = CSRFProtectForm()

    if username == session.get('username', None):
        user = User.query.get_or_404(username)
        return render_template('user_profile.html', user=user, form=form)

    else:
        flash('You are not authorized for this page!')
        return redirect('/')



@app.post('/logout')
def logout_user():
    """Route for logging out users."""
    form = CSRFProtectForm()

    if form.validate_on_submit():
        print("logging out, form validation if statement")

        session.pop('username', None)

    # could be more aggressive if form fails validation, error
    return redirect('/')


@app.route('/notes/<int:id>/update', methods=['GET','POST'])
def handle_note_update(id):
    """Render note update form and handle update"""
    form = updateNote()
    note = Note.query.get_or_404(id)

    if form.validate_on_submit():
        note.title= form.title.data
        note.content = form.content.data
        db.session.commit()
        redirect(f"/users/{note.owner_username}")

    return render_template("update_note.html", form=form)


