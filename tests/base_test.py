from bucketlist import create_app, db
from bucketlist.models import User, Bucketlist, Item

import json
import unittest

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        """ this function creates the base test"""

        self.app = create_app(config_name="development")

        self.user1 = User(username="ktumbo",
                          email="ktumbo@gmail.com",
                          password="password")

        self.user2 = User(username="georgreen",
                          email="geo@gmail.com",
                          password="password1")

        self.bucketlist1 = Bucketlist(name="Work goals",
                                      description="Things To achieve at work",
                                      owner_id=1)

        self.bucketlist2 = Bucketlist(name="Life Goals",
                                      description="Things To Achieve in Life",
                                      owner_id=1)

        self.item1 = Item(item_name="Be A Python and Js Ninja",
                          item_description="Be a pro in flask, Django, Angular, React and vue ",
                          owner_id=1,
                          bucketlist_id=1)

        self.item2 = Item(item_name="Be a rockstar",
                          item_description="Learn how to play slipknot songs proficiently",
                          owner_id=1,
                          bucketlist_id=2)

        with self.app.app_context():

            db.create_all()

    def tearDown(self):
        """ removes resources once tests have run """
        with self.app.app_context():

            db.session.remove()
            db.drop_all()
