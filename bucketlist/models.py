import datetime
from bucketlist import db


class User(db.Model):

    """ creates a user """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    bucketlists = db.relationship('Bucketlist', backref='users', lazy='dynamic')
    items = db.relationship('Item', backref='user', lazy='dynamic')


    def __repr__(self):
        return '<User %r>' % self.username

class Bucketlist(db.Model):

    """ creates a bucketlist """

    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modifed = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    items = db.relationship('Item', backref='bucketlist', lazy='dynamic')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<List name %r>' % self.name

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
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Item Name %r>' % self.item_name