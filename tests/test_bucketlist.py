import json
from tests.base_test import BaseTestCase


class BucketListTests(BaseTestCase):
    """ Test cases for Bucketlist functionality"""

    def test_create_bucketlist_succesfully(self):
        """
        Test API can create a bucketlist (POST request)
        """

        self.data = {
            "name":"Midlife goals",
            "description":"My achievement by 40",
            "owner_id": 1
        }

        # Make the post request and get the response
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.data,
                                      headers=self.my_header)
        self.assertEqual(response.status_code, 201)
        self.assertIn("You have succesfully created a bucketlist", str(response.data))

    def test_create_bucketlist_without_correct_access_token(self):
        """
        Test API cannot create a bucketlist without token
        """
        access_token = "gjlnrngnrganerngrng596436843tdkfdsfkndks"

        self.data = {
            "name":"Midlife goals",
            "description":"My achievement by 40",
            "owner_id": 1
        }
        # Make the post request and get the response
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.data,
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid Token", str(response.data))

    def test_invalid_bucketlist_name_format(self):
        """
        Test API cannot create a bucketlist when name is invalid format (POST request)
        """

        self.data = {
            "name":"))(*",
            "description":"Things to do in 2017",
            "owner_id": 1
        }
        # Make the post request and get the response
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.data,
                                      headers=self.my_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Sorry Invalid name format. please put a valid name", str(response.data))

    def test_bucketlist_creation_when_missing_name(self):
        """
        Test API cannot create a bucketlist when name is missing (POST request)
        """

        self.data = {
            "description":"Things to do in 2017",
            "owner_id": 1
        }

        # Make the post request and get the response
        response = self.client().post('/api/v1.0/bucketlists/', data=self.data,
                                      headers=self.my_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn("bucketlist missing name", str(response.data))


    def test_bucketlist_creation_when_missing_description(self):
        """
        Test API cannot create a bucketlist when description is missing
        (POST request)
        """

        self.data = {
            "name":"20:20 vision",
            "owner_id": 1
        }

        # Make the post request and get the response
        response = self.client().post('/api/v1.0/bucketlists/', data=self.data,
                                      headers=self.my_header)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Bucketlist desscription missing", str(response.data))

    def test_creation_of_duplicate_bucketlist(self):
        """
        Test API cannot create a duplicate bucketlist (POST request)
        """

        self.data = {
            "name":"Midlife goals",
            "description":"My achievement by 40",
            "owner_id": 1
        }

        # Make the post request and get the response
        response1 = self.client().post('/api/v1.0/bucketlists/', data=self.data,
                                       headers=self.my_header)

        self.data2 = {
            "name":"Midlife goals",
            "description":"My achievement by 40",
            "owner_id": 1
        }
        response2 = self.client().post('/api/v1.0/bucketlists/', data=self.data,
                                       headers=self.my_header)

        self.assertEqual(response2.status_code, 409)
        self.assertIn("That bucketlist already exists", str(response2.data))

    def test_retrive_all_bucketlists(self):
        """
        Test API can return a list of all bucketlists
        (GET request)
        """

        # Make the post request and get the response
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.bucketlist,
                                      headers=self.my_header)
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.bucketlists2,
                                      headers=self.my_header)
        response = self.client().get("/api/v1.0/bucketlists/",
                                     headers=self.my_header)
        self.assertIn("Work goals", str(response.data))
        self.assertIn("Life Goals", str(response.data))

    def test_get_bucketlist_using_id(self):
        """
        Test API can return an existing bucketlist using id as a parameter
        (GET request)
        """
        # Make the post request and get the response
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.bucketlist,
                                      headers=self.my_header)

        response = self.client().get("/api/v1.0/bucketlists/1",
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("IEBC Goals", str(response.data))
        self.assertIn("Things IEBC needs to achieve", str(response.data))

    def test_can_get_bucketlist_by_searching_name(self):
        """
        Test Api can retrive existing bucketlist using name as a parameter
        (GET request)
        """
        # Make the post request and get the response
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.bucketlists2,
                                      headers=self.my_header)
        response = self.client().get("/api/v1.0/bucketlists/?q=life",
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Life Goals", str(response.data))
        self.assertIn("Things To Achieve in Life", str(response.data))

    def test_get_nonexisting_bucketlist(self):
        """
        Test API returns error message if a bucketlist does not exist
        (GET request)
        """

        response = self.client().get("/api/v1.0/bucketlists/66686768",
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 404)
        self.assertIn("404 Not Found", str(response.data))

    def test_update_bucketlist(self):
        """
        Test API can create update bucketlist (PUT request)
        """

        self.data = {
            "name":"Update goals",
            "description":"at work(updated)",
            "owner_id": 1
        }

        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.data,
                                      headers=self.my_header)
        self.data = {
            "name":"Update work goals",
            "description":"Things To achieve at work(updated)",
            "owner_id": 1
        }

        response = self.client().put("/api/v1.0/bucketlists/1",
                                     data=self.data,
                                     headers=self.my_header)

        self.assertEqual(response.status_code, 200)
        self.assertIn("You have succesfully updated a bucketlist", str(response.data))

    def test_update_nonexisting_bucketlist(self):
        """
        Test API cannot update a bucketlist if bucketlist is missing or does not exist
        (PUT request)
        """

        self.data = {
            "name":"Update work goals",
            "description":"Things To achieve at work(updated)",
            "owner_id": 1
        }

        response = self.client().put("/api/v1.0/bucketlists/1088", data=self.data,
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 404)
        self.assertIn("404 Not Found", str(response.data))

    def test_cannot_update_bucketlist_when_missing_name(self):
        """
        Test API cannot update a bucketlist if bucketlist is missing name
        (PUT request)
        """
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.bucketlists2,
                                      headers=self.my_header)
        self.data = {
            "description":"Things To achieve at work(updated)",
            "owner_id": 1
        }

        response = self.client().put("/api/v1.0/bucketlists/1", data=self.data,
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn("bucketlist missing name", str(response.data))

    def test_cannot_update_bucketlist_when_missing_description(self):
        """
        Test API cannot update a bucketlist if bucketlist is missing description
        (PUT request)
        """
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.bucketlists2,
                                      headers=self.my_header)
        self.data = {
            "name":"Update work goals",
            "owner_id": 1
        }

        response = self.client().put("/api/v1.0/bucketlists/1", data=self.data,
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Bucketlist desscription missing", str(response.data))
    
    def test_cannot_update_bucketlist_when_name_is_invalid_format(self):
        """
        Test API cannot update a bucketlist if bucketlist is missing description
        (PUT request)
        """
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.bucketlists2,
                                      headers=self.my_header)
        self.data = {
            "name":"&&(&)((&&(&",
            "description":"Things To achieve at work(updated)",
            "owner_id": 1
        }

        response = self.client().put("/api/v1.0/bucketlists/1", data=self.data,
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Sorry Invalid name format. please put a valid name", str(response.data))

    def test_deletion_of_bucketlist(self):
        """
        Test API can delete a bucketlist
        (DELETE request)
        """
        response = self.client().post('/api/v1.0/bucketlists/',
                                      data=self.bucketlists2,
                                      headers=self.my_header)

        response2 = self.client().delete("/api/v1.0/bucketlists/1",
                                         headers=self.my_header)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("bucketlist 1 deleted successfully", str(response2.data))

    def test_deletion_of_nonexistant_bucketlist(self):
        """
        Test API cannot delete a bucketlist that doesn't exist (DELETE request)
        """

        response = self.client().delete("/api/v1.0/bucketlists/290834",
                                        headers=self.my_header)
        self.assertEqual(response.status_code, 404)
        self.assertIn("404 Not Found", str(response.data))
