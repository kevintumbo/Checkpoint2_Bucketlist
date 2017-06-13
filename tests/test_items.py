import json
from tests.base_test import BaseTestCase


class BueketListItemsTests(BaseTestCase):

    """ Test cases for bucketlist item functionality """

    def test_succesful_creation_of_bucketlist_item(self):

        """
        Test API can succesfully create a bucketlist item (POST request)
        """

        self.data = {
            "item_name":"Trance Music",
            "item_description":"Create deadmaus trance remakes",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      headers=self.my_header,
                                      data=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("You have succesfully created a bucketlist item", str(response.data))

    def test_create_item_when_missing_title(self):

        """
        Test API cannot create a bucketlist item when name is missing
        (POST request)
        """

        self.data = {
            "item_name":"",
            "item_description":"Buy a guitar",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn("bucketlist item missing name", str(response.data))

    def test_create_item_when_name_is_in_invalid_format(self):
        """
         Test API cannot create a bucketlist item when name is in invalid format
        (POST request)
        """

        self.data = {
            "item_name":"*&*(^^^*^)*^))(&(",
            "item_description":"Blackhole sun won't you wash me away?",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Sorry Invalid name format. please put a valid name", str(response.data))

    def test_create_bucketlist_item_when_missing_description(self):
        """
        Test API cannot create a bucketlist item when description is missing
        (POST request)
        """

        self.data = {
            "item_name":"snowboard",
            "item_description":"",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Bucketlist item description missing", str(response.data))

    def test_creation_of_duplicate_bucketlist_item(self):

        """
        Test API cannot create a duplicate bucketlist item (POST request)
        """

        self.data = {
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)
        self.data = {
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)

        self.assertEqual(response.status_code, 409)
        self.assertIn("That bucketlist item already exists", str(response.data))

    def test_creation_of_bucketlist_item_in_nonexistant_bucketlist(self):

        """
        Test API cannot create a bucketlist item in a bucketlist that doesn't exist(POST request)
        """

        self.data = {
            "item_name":"wagwan",
            "item_description":"Testing 1 2",
            "owner_id": 1,
            "bucketlist_id":67
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/67/items/",
                                      data=self.data,
                                      headers=self.my_header)

        self.assertEqual(response.status_code, 404)
        self.assertIn("Bucketlist does not exist", str(response.data))

    def test_update_bucketlist_item(self):
        """
        Test API can edit a bucketlist item (PUT request)
        """

        self.data = {
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)

        self.data = {
            "item_name":"Be A Python and Ruby Ninja updated",
            "item_description":"Be a pro in flask, Django and Ruby on Rails",
            "is_done": 1
        }

        # Make the post request and get the response
        response = self.client().put("/api/v1.0/bucketlists/1/items/1",
                                     data=self.data,
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("You have succesfully updated a bucketlist item", str(response.data))

    def test_update_nonexisting_bucketlist_item(self):
        """
        Test API cannot update a bucketlist item that doesn't exist (PUT request)
        """

        self.data = {
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue"
        }

        # Make the post request and get the response
        response = self.client().put("/api/v1.0/bucketlists/1/items/100503953",
                                     data=self.data,
                                     headers=self.my_header)

        self.assertEqual(response.status_code, 404)
        self.assertIn("Bucketlist item does not exist", str(response.data))


    def test_can_delete_bucketlist_item(self):
        """
        Test API can delete an existing bucketlist (DELETE request)
        """

        self.data = {
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)

        response = self.client().delete("/api/v1.0/bucketlists/1/items/1",
                                        headers=self.my_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("bucketlist item 1 deleted successfull", str(response.data))

    def test_delete_nonexistant_bucketlist_item(self):
        """
        Test API cannot delete a bucketlist item that does not exist (DELETE request)
        """

        self.data = {
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)

        response = self.client().delete("/api/v1.0/bucketlists/1/items/9980803",
                                        headers=self.my_header)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Bucketlist item does not exist", str(response.data))

    def test_change_item_status_to_done(self):
        """
        Test API can change status of bucketlist item to done (PUT request)
        """

        self.data = {
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)

        self.data = {
            "item_name":"Be A Python and Ruby Ninja",
            "item_description":"Be a pro in flask, Django and Ruby on Rails",
            "is_done": 1
        }

        # Make the post request and get the response
        response = self.client().put("/api/v1.0/bucketlists/1/items/1",
                                     data=self.data,
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("You have succesfully updated a bucketlist item", str(response.data))

    def test_change_item_status_to_not_done(self):
        """
        Test API can change status a bucketlist item to not done (PUT request)
        """

        self.data = {
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue",
            "owner_id": 1,
            "bucketlist_id":1
        }

        # Make the post request and get the response
        response = self.client().post("/api/v1.0/bucketlists/1/items/",
                                      data=self.data,
                                      headers=self.my_header)

        self.data = {
            "item_name":"Be A Python and Ruby Ninja",
            "item_description":"Be a pro in flask, Django and Ruby on Rails",
            "is_done": 1
        }

        # Make the post request and get the response
        response = self.client().put("/api/v1.0/bucketlists/1/items/1",
                                     data=self.data,
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("You have succesfully updated a bucketlist item", str(response.data))

        self.data = {
            "item_name":"Be A Python and Ruby Ninja",
            "item_description":"Be a pro in flask, Django and Ruby on Rails",
            "is_done": 0
        }

        # Make the post request and get the response
        response = self.client().put("/api/v1.0/bucketlists/1/items/1",
                                     data=self.data,
                                     headers=self.my_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("You have succesfully updated a bucketlist item", str(response.data))
