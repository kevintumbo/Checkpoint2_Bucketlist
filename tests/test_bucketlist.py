import json
from tests.base_test import BaseTestCase

URL_bucketlist = '/api/v1.0/bucketlists/'


class BucketListTests(BaseTestCase):
    """ Test cases for Bucketlist functionality"""

    def test_for_succesfull_creation_of_bucketlist(self):
        """
        Test API can create a bucketlist (POST request)
        """

        data = json.dumps({
            "name":" Midlife goals",
            "description":"My achievement by 40",
            "owner_id": 1
        })

        # Make the post request and get the response
        response = self.app.post(URL_bucketlist, data, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "You have succesfully created a bucketlist")

    def test_bucketlist_creation_when_missing_name(self):
        """
        Test API cannot create a bucketlist when name is missing (POST request)
        """
        data = json.dumps({
            "name":" ",
            "description":"Things to do in 2017",
            "owner_id": 1
        })

        # Make the post request and get the response
        response = self.app.post(URL_bucketlist, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Bucketlist name missing")

    def test_bucketlist_creation_when_missing_description(self):
        """
        Test API cannot create a bucketlist when description is missing
        (POST request)
        """

        data = json.dumps({
            "name":"20:20 vision",
            "description":" ",
            "owner_id": 1
        })

        # Make the post request and get the response
        response = self.app.post(URL_bucketlist, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Bucketlist desscription missing")

    def test_creation_of_duplicate_bucketlist(self):
        """
        Test API cannot create a duplicate bucketlist (POST request)
        """

        data = json.dumps({
            "name":"Work goals",
            "description":"Things To achieve at work",
            "owner_id": 1
        })

        # Make the post request and get the response
        response = self.app.post(URL_bucketlist, data, content_type="application/json")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "That bucketlist already exists")

    def test_get_bucketlist_using_id(self):
        """
        Test API can return an existing bucketlist using id as a parameter
        (GET request)
        """
        response = self.app.get("/api/v1.0/bucketlists/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()['name'], "Work goals")
        self.assertIn(response.json()['description'], "Things To achieve at work")

    def test_can_get_bucketlist_by_searching_name(self):
        """
        Test Api can retrive existing bucketlist using name as a parameter
        (GET request)
        """
        response = self.app.get("/api/v1.0/bucketlists/Life+Goals")
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()['name'], "Life Goals")
        self.assertIn(response.json()['description'], "TThings To Achieve in Life")

    def test_get_nonexisting_bucketlist(self):
        """
        Test API returns error message if a bucketlist does not exist
        (GET request)
        """
        response = self.app.get("/api/v1.0/bucketlists/66686768")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "bucketlist does not exist")

    def test_get_bucketlist_without_id_or_name(self):
        """
        Test API returns error if missing id or name in url
        (GET request)
        """
        response = self.app.get("/api/v1.0/bucketlists")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "missing bucketlist id or name")

    def test_update_bucketlist(self):
        """
        Test API can create update bucketlist (PUT request)
        """
        data = json.dumps({
            "name":"Update work goals",
            "description":"Things To achieve at work(updated)",
            "owner_id": 1
        })

        response = self.app.put("/api/v1.0/bucketlists/1", data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['Message'], "You have succesfully updated a bucketlist")

    def test_update_nonexisting_bucketlist(self):
        """
        Test API cannot update a bucketlist if bucketlist is missing or does not exist
        (PUT request)
        """
        data = json.dumps({
            "name":"Update work goals",
            "description":"Things To achieve at work(updated)",
            "owner_id": 1
        })

        response = self.app.put("/api/v1.0/bucketlists/1088", data, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "bucketlist does not exist")

    def test_deletion_of_bucketlist(self):
        """
        Test API can delete a bucketlist
        (DELETE request)
        """
        response = self.app.delete("/api/v1.0/bucketlists/2")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "bucketlist has been deleted")

    def test_deletion_of_nonexistant_bucketlist(self):
        """
        Test API cannot delete a bucketlist that doesn't exist (DELETE request)
        """
        response = self.app.delete("/api/v1.0/bucketlists/290834")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], "bucketlist does not exist")
