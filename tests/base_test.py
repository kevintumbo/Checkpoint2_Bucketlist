from bucketlist import create_app, db
from bucketlist.models import User, Bucketlist, Item

import json
import unittest

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        """ this function creates the base test"""

        self.app = create_app(config_name="development")
        self.client = self.app.test_client

        self.user1 = {"username":"ktumbo",
                      "email":"ktumbo@gmail.com",
                      "password":"password"
                     }


        self.bucketlist = {"name":"Work goals",
                           "description":"Things To achieve at work",
                           "owner_id": 1
                          }

        self.bucketlists2 = {"name":"Life Goals",
                             "description":"Things To Achieve in Life",
                             "owner_id": 1
                            }

        self.item1 = {"item_name":"Be A Python and Js Ninja",
                      "item_description":"Be a pro in flask, Django, Angular, React and vue ",
                      "owner_id": 1,
                      "bucketlist_id": 1
                     }

        self.item2 = {"item_name":"Be a rockstar",
                      "item_description":"Learn how to play slipknot songs proficiently",
                      "owner_id":1,
                      "bucketlist_id":1
                     }

        with self.app.app_context():

            db.create_all()

    def tearDown(self):
        """ removes resources once tests have run """
        with self.app.app_context():

            db.session.remove()
            db.drop_all()
