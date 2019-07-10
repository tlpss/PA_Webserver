from server import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from server import login


# M-N relation
FeederUsers = db.Table('feederusers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('feeder_id', db.Integer, db.ForeignKey('feeder.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    feeders = db.relationship(
        'Feeder', secondary=FeederUsers,
        primaryjoin=(FeederUsers.c.user_id == id),
        secondaryjoin=(FeederUsers.c.feeder_id == id),
        backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self,password):
        self.password_hash  = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Feeder(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    modified = db.Column(db.Boolean) # meant to signal a change in the schedule to the feeder
    feed_moments = db.relationship('FeedMoment',backref = 'Feeder', lazy= 'dynamic' )

    def __repr__(self):
        return f'Feeder {self.id}'


class FeedMoment(db.Model):
    feeder_id = db.Column(db.Integer, db.ForeignKey('feeder.id'),primary_key = True)
    timestamp = db.Column(db.Time, primary_key=True, unique=True)
    amount = db.Column(db.Integer)

    def __repr__(self):
        return f'FeedMoment {self.feeder_id} - {self.timestamp}'




