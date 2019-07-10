from server import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from server import login
from datetime import datetime


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

    feeders = db.relationship('Feeder', secondary=FeederUsers, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

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
    feed_moments = db.relationship('FeedMoment',backref = 'Feeder', lazy= 'dynamic' )

    def __repr__(self):
        return f'Feeder {self.id}'

    def get_lastupdate(self):
        return self.feed_moments.order_by(FeedMoment.last_updated.desc()).first().last_updated

    def get_next_moment(self):
        now  = datetime.now()
        current = now.hour*60  +now.minute
        print(current)
        result  = self.feed_moments.filter(FeedMoment.feed_time > current).order_by(FeedMoment.feed_time).all()
        if len(result) > 0:
            return result[0]
        else:
            return self.feed_moments.order_by(FeedMoment.feed_time).all()[0] # last feedmoment of the day , next moment is first of next day

class FeedMoment(db.Model):
    feeder_id = db.Column(db.Integer, db.ForeignKey('feeder.id'))
    feedmoment_id = db.Column(db.Integer, primary_key=True)
    feed_time = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.now)  # meant to signal a change in the schedule to the feeder
    amount = db.Column(db.Integer)

    def __repr__(self):
        return f'FeedMoment {self.Feeder} - {self.feed_time}'


    def setFeedTime(self,hours, minutes):
        self.feed_time = hours * 60 + minutes

    def getFeedTime(self):
        minutes = self.feed_time % 60
        hours = int ((self.feed_time - minutes) / 60)
        return {'hours': hours, 'minutes': minutes}

