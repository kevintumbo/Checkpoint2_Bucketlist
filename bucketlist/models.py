import datetime
from datetime import timedelta
from bucketlist import db
from flask import current_app
from flask_bcrypt import Bcrypt
import jwt


class User(db.Model):

    """ creates a user """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    bucketlists = db.relationship('Bucketlist', backref='users', lazy='dynamic')
    items = db.relationship('Item', backref='users', lazy='dynamic')

    def __init__(self, username, email, password):
        """Initialize the user with username, email and a password."""
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """

        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.datetime.utcnow()+ timedelta(minutes=5),
                'iat': datetime.datetime.utcnow(),
                'sub': id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        
        return '<User %r>' % self.username


class Bucketlist(db.Model):

    """ creates a bucketlist """

    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modifed = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                             onupdate=datetime.datetime.utcnow)
    items = db.relationship('Item', backref='bucketlist', lazy='dynamic', cascade='delete')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(
            self.name,
            self.description,
            self.date_created,
            self.date_modifed,
            self.population
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
class Item(db.Model):

    """ creates a bucketlist item """

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(80), unique=True)
    item_description = db.Column(db.Text)
    is_done = db.Column(db.Boolean(), nullable=False, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                              onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Item Name %r>' % self.item_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()