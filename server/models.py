from server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'


# M-N relation
FeederUsers = db.Table('feederusers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('feeder_id', db.Integer, db.ForeignKey('petfeeder.id'), primary_key=True)
)


class PetFeeder(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    modified = db.Column(db.Boolean) # meant to signal a change in the schedule to the feeder
    feed_moments = db.relationship('FeedMoment',backref = 'petfeeder', lazy= 'dynamic' )

    def __repr__(self):
        return f'PetFeeder {self.id}'



class FeedMoment(db.Model):
    feeder_id = db.Column(db.Integer, db.ForeignKey('petfeeder.id'),primary_key = True)
    timestamp = db.Column(db.Time, primary_key=True, unique=True)
    amount = db.Column(db.Integer)

    def __repr__(self):
        return f'FeedMoment {self.feeder_id} - {self.timestamp}'

