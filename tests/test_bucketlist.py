import json
from tests.base_test import BaseTestCase

URL_bucketlist = '/api/v1.0/bucketlists/'


class BucketListTests(BaseTestCase):
    """ Test cases for Bucketlist functionality"""

    def register_user(self):
        user_data = {
            "username": "ktumbo",
            "email": "user@gmail.com",
            "password": "user"
        }
        return self.client().post('/api/v1.0/auth/register', data=user_data)

    def login_user(self):
        user_data = {
            "email": "user@gmail.com",
            "password": "user"
        }
        return self.client().post('/api/v1.0/auth/login', data=user_data)


    def test_create_bucketlist_succesfully(self):
        """
        Test API can create a bucketlist (POST request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.data = {
            "name":"Midlife goals",
            "description":"My achievement by 40",
            "owner_id": 1
        }

        # Make the post request and get the response
        response = self.client().post(URL_bucketlist,
                                      data=self.data,
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        self.assertIn("You have succesfully created a bucketlist", str(response.data))

    def test_create_bucketlist_without_correct_access_token(self):
        """
        Test API cannot create a bucketlist without token
        """
        self.register_user()
        result = self.login_user()
        access_token = "gjlnrngnrganerngrng596436843tdkfdsfkndks"

        self.data = {
            "name":"Midlife goals",
            "description":"My achievement by 40",
            "owner_id": 1
        }
        # Make the post request and get the response
        response = self.client().post(URL_bucketlist,
                                      data=self.data,
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid Token", str(response.data))


    def test_bucketlist_creation_when_missing_name(self):
        """
        Test API cannot create a bucketlist when name is missing (POST request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.data = {
            "description":"Things to do in 2017",
            "owner_id": 1
        }

        # Make the post request and get the response
        response = self.client().post(URL_bucketlist, data=self.data,
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 400)
        self.assertIn("bucketlist missing name", str(response.data))


    def test_bucketlist_creation_when_missing_description(self):
        """
        Test API cannot create a bucketlist when description is missing
        (POST request)
        """

        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.data = {
            "name":"20:20 vision",
            "owner_id": 1
        }

        # Make the post request and get the response
        response = self.client().post(URL_bucketlist, data=self.data,
                                      headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(response.status_code, 400)
        self.assertIn("Bucketlist desscription missing", str(response.data))

    def test_creation_of_duplicate_bucketlist(self):
        """
        Test API cannot create a duplicate bucketlist (POST request)
        """

        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.data = {
            "name":"Midlife goals",
            "description":"My achievement by 40",
            "owner_id": 1
        }

        # Make the post request and get the response
        response1 = self.client().post(URL_bucketlist, data=self.data,
                                       headers=dict(Authorization="Bearer " + access_token))

        self.data2 = {
            "name":"Midlife goals",
            "description":"My achievement by 40",
            "owner_id": 1
        }
        response2 = self.client().post(URL_bucketlist, data=self.data,
                                       headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(response2.status_code, 409)
        self.assertIn("That bucketlist already exists", str(response2.data))

    def test_retrive_all_bucketlists(self):
        """
        Test API can return a list of all bucketlists
        (GET request)
        """

        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        # Make the post request and get the response
        response = self.client().post(URL_bucketlist,
                                      data=self.bucketlist,
                                      headers=dict(Authorization="Bearer " + access_token))
        response = self.client().post(URL_bucketlist,
                                      data=self.bucketlists2,
                                      headers=dict(Authorization="Bearer " + access_token))
        response = self.client().get("/api/v1.0/bucketlists/",
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertIn("Work goals", str(response.data))
        self.assertIn("Life Goals", str(response.data))

    def test_get_bucketlist_using_id(self):
        """
        Test API can return an existing bucketlist using id as a parameter
        (GET request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        # Make the post request and get the response
        response = self.client().post(URL_bucketlist,
                                      data=self.bucketlist,
                                      headers=dict(Authorization="Bearer " + access_token))

        response = self.client().get("/api/v1.0/bucketlists/1",
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Work goals", str(response.data))
        self.assertIn("Things To achieve at work", str(response.data))

    def test_can_get_bucketlist_by_searching_name(self):
        """
        Test Api can retrive existing bucketlist using name as a parameter
        (GET request)
        """
        response = self.client().get("/api/v1.0/bucketlists/Life+Goals")
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()['name'], "Life Goals")
        self.assertIn(response.json()['description'], "TThings To Achieve in Life")

    def test_get_nonexisting_bucketlist(self):
        """
        Test API returns error message if a bucketlist does not exist
        (GET request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().get("/api/v1.0/bucketlists/66686768",
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)
        self.assertIn("404 Not Found", str(response.data))

    def test_update_bucketlist(self):
        """
        Test API can create update bucketlist (PUT request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.data = {
            "name":"Update goals",
            "description":"at work(updated)",
            "owner_id": 1
        }

        response = self.client().post(URL_bucketlist,
                                      data=self.data,
                                      headers=dict(Authorization="Bearer " + access_token))
        self.data = {
            "name":"Update work goals",
            "description":"Things To achieve at work(updated)",
            "owner_id": 1
        }

        response = self.client().put("/api/v1.0/bucketlists/1",
                                     data=self.data,
                                     headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(response.status_code, 200)
        self.assertIn("You have succesfully updated a bucketlist", str(response.data))

    def test_update_nonexisting_bucketlist(self):
        """
        Test API cannot update a bucketlist if bucketlist is missing or does not exist
        (PUT request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.data = {
            "name":"Update work goals",
            "description":"Things To achieve at work(updated)",
            "owner_id": 1
        }

        response = self.client().put("/api/v1.0/bucketlists/1088", data=self.data,
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)
        self.assertIn("404 Not Found", str(response.data))

    def test_deletion_of_bucketlist(self):
        """
        Test API can delete a bucketlist
        (DELETE request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.data = {
            "name":"Update work goals",
            "description":"Things To achieve at work(updated)",
            "owner_id": 1
        }

        response = self.client().post(URL_bucketlist, data=self.data,
                                      headers=dict(Authorization="Bearer " + access_token))

        response2 = self.client().delete("/api/v1.0/bucketlists/1",
                                         headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response2.status_code, 200)
        self.assertIn("bucketlist 1 deleted successfully", str(response2.data))

    def test_deletion_of_nonexistant_bucketlist(self):
        """
        Test API cannot delete a bucketlist that doesn't exist (DELETE request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().delete("/api/v1.0/bucketlists/290834",
                                        headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)
        self.assertIn("404 Not Found", str(response.data))
