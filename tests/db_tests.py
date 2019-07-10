import unittest
from server import app, db
from server.models import User, Feeder, FeederUsers, FeedMoment


class UserModelCase(unittest.TestCase):
    def setUp(self):
        # create temporal DB in memory!
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        user  = User(username="test1",email="test.t@gm.com")
        user.set_password("fake1")
        db.session.add(user)
        db.session.commit()
        user = User.query.get(1)
        self.assertTrue(user.check_password("fake1"))
        self.assertFalse(user.set_password("fake2"))

    def test_Feeder_Feedmoment(self):
        feeder = Feeder()
        moment1 = FeedMoment(amount  = 1, Feeder  = feeder)
        moment2 = FeedMoment(amount  =2 ,Feeder  = feeder)

        self.assertTrue(len(feeder.feed_moments.all()) == 2)
        self.assertTrue(feeder.feed_moments[0].amount == 1)


    def test_Feeder_User(self):
        user1 = User(username="test1")
        user2 = User(username="test2")

        feeder = Feeder(modified=False)
        feeder.users.append(user1)
        user2.feeders.append(feeder)

        self.assertTrue( len(feeder.users.all()) == 2)





