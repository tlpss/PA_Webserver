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
    name = db.Column(db.String)
    feed_moments = db.relationship('FeedMoment',backref = 'Feeder', lazy= 'dynamic')
    secret_key = db.Column(db.String)

    def __repr__(self):
        return f'Feeder {self.id}'

    def get_lastupdate(self):
        return self.feed_moments.order_by(FeedMoment.last_updated.desc()).first().last_updated

    def get_next_moment(self,time= None):
        if time is None:
            now  = datetime.now()
            current = now.hour*60  +now.minute
        else:
            current = time
        print(current)
        result  = self.feed_moments.filter(FeedMoment.feed_time > current).order_by(FeedMoment.feed_time).all()
        if len(result) > 0:
            return result[0]
        else:
            list = self.feed_moments.order_by(FeedMoment.feed_time).all() # last feedmoment of the day , next moment is first of next day
            if len(list)> 0:
                return list[0]
            else:
                return FeedMoment(amount= 0) # placeholder

    def get_all_moments_updated_between(self, first, second):
        list = []
        print(first)
        print(second)
        for moment in self.feed_moments:
            #print(moment)
            #list.append(moment.get_json_dict())
            #print(moment.last_updated > first)
            #print(moment.last_updated < second)
            if moment.last_updated >= first and moment.last_updated <= second:
                list.append(moment.get_json_dict())
        return list


    def get_feeder_from_hash(hash):
        #TODO: this is a test implementation for plaintext
        return Feeder.query.filter_by(name = hash).first()

class FeedMoment(db.Model):
    feeder_id = db.Column(db.Integer, db.ForeignKey('feeder.id'))
    feedmoment_id = db.Column(db.Integer, primary_key=True)
    feed_time = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.now)  # meant to signal a change in the schedule to the feeder
    amount = db.Column(db.Integer)

    def __repr__(self):
        return f'FeedMoment {self.Feeder} - {self.feed_time}'

    def get_json_dict(self):
        return {'feed_time' : self.getFeedTime(), 'amount' : self.amount, 'last_updated' : self.last_updated}

    def setFeedTime(self,hours, minutes):
        self.feed_time = hours * 60 + minutes

    def getFeedTime(self):
        minutes = self.feed_time % 60
        hours = int ((self.feed_time - minutes) / 60)
        return {'hours': hours, 'minutes': minutes}

