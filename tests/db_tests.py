import unittest
from server import app, db
from server.models import User, Feeder, FeederUsers, FeedMoment
from datetime import datetime

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
        db.session.add(feeder)
        db.session.add(moment1)
        db.session.add(moment2)
        db.session.commit()
        self.assertTrue(len(feeder.feed_moments.all()) == 2)
        self.assertTrue(feeder.feed_moments[0].amount == 1)


    def test_Feeder_User(self):
        user1 = User(username="test1")
        user2 = User(username="test2")

        feeder = Feeder()
        feeder.users.append(user1)
        user2.feeders.append(feeder)

        db.session.add(feeder)
        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()

        self.assertTrue( len(feeder.users.all()) == 2)
        self.assertEqual(user1.feeders[0],feeder)



    def test_Feederusage(self):
        user1 = User(username="test1")
        feeder =  Feeder()
        #feeder.users.append(user1)

        moment1 = FeedMoment(amount= 2, Feeder=feeder)
        moment1.setFeedTime(5,12)

        moment2 = FeedMoment(amount= 3, Feeder=feeder)
        moment2.setFeedTime(14,15)

        db.session.add(feeder)
        db.session.add(moment1)
        db.session.add(moment2)
        db.session.commit()
        #print(feeder.get_lastupdate())
        self.assertEqual(moment2.last_updated,feeder.get_lastupdate()) #test global last update
        #!! current time is important!
        time = datetime.now().hour*60 + datetime.now().minute
        print(time)
        if time > moment2.feed_time:
            self.assertEqual(feeder.get_next_moment(),moment1)
        else:
            self.assertEqual(feeder.get_next_moment(),moment2)




