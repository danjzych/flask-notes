from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    username = db.Column(
        db.String(20),
        primary_key=True
    )
    password = db.Column(
        db.String(100),
        nullable=False
    )
    email = db.Column(
        EmailType(50),
        nullable=True
    )
    first_name = db.Column(
        db.String(30),
        nullable=False
    )
    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a new user in notes app."""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username,
                   password=hashed,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user in notes app."""

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False


class Note(db.Model):
    """Note model"""

    __tablename__ = 'notes'

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    owner_username = db.Column(
        db.ForeignKey("users.username"),
        nullable=False
    )

    user = db.relationship("User", backref="notes")