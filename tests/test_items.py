import json
from tests.base_test import BaseTestCase

# POST /bucketlists/<id>/items/
# PUT /bucketlists/<id>/items/<item_id>
# DELETE /bucketlists/<id>/items/<item_id>


class BueketListItemsTests(BaseTestCase):

    """ Test cases for bucketlist item functionality """

    def test_succesful_creation_of_bucketlist_item(self):

        """
        Test API can succesfully create a bucketlist item (POST request)
        """

        data = json.dumps({
            "item_name":" Trance Music",
            "item_description":"Create deadmaus trance remakes",
            "owner_id": 1,
            "bucketlist_id":1
        })

        # Make the post request and get the response
        response = self.app.post("/api/v1.0/bucketlists/1/items/",
                                 data, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "bucketlist item succesfully created ")

    def test_create_item_when_missing_title(self):

        """
        Test API cannot create a bucketlist item when name is missing
        (POST request)
        """
        data = json.dumps({
            "item_name":" ",
            "item_description":"Buy a guitar",
            "owner_id": 1,
            "bucketlist_id":2
        })

        # Make the post request and get the response
        response = self.app.post("/api/v1.0/bucketlists/2/items/",
                                 data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Bucketlist item title missing")

    def test_create_item_when_name_is_in_invalid_format(self):
        """
         Test API cannot create a bucketlist item when name is in invalid format
        (POST request)
        """

        data = json.dumps({
            "item_name":"slipknot tings",
            "item_description":" *&*(^^^*^)*^))(&(",
            "owner_id": 1,
            "bucketlist_id":2
        })

        # Make the post request and get the response
        response = self.app.post("/api/v1.0/bucketlists/2/items/",
                                 data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Bucketlist item in invalid format")

    def test_create_bucketlist_item_when_missing_description(self):
        """
        Test API cannot create a bucketlist item when description is missing
        (POST request)
        """

        data = json.dumps({
            "item_name":"snowboard",
            "item_description":" ",
            "owner_id": 1,
            "bucketlist_id":1
        })

        # Make the post request and get the response
        response = self.app.post("/api/v1.0/bucketlists/1/items/",
                                 data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Bucketlist item missing description")

    def test_creation_of_duplicate_bucketlist_item(self):

        """
        Test API cannot create a duplicate bucketlist item (POST request)
        """
        data = json.dumps({
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue",
            "owner_id": 1,
            "bucketlist_id":1
        })

        # Make the post request and get the response
        response = self.app.post("/api/v1.0/bucketlists/1/items/1",
                                 data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], "Bucketlist item already exists")

    def test_creation_of_bucketlist_item_in_nonexistant_bucketlist(self):

        """
        Test API cannot create a bucketlist item in a bucketlist that doesn't exist(POST request)
        """
        data = json.dumps({
            "item_name":"wagwan",
            "item_description":"Testing 1 2",
            "owner_id": 1,
            "bucketlist_id":67
        })

        # Make the post request and get the response
        response = self.app.post("/api/v1.0/bucketlists/67/items/",
                                 data, content_type="application/json")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], "Bucketlist does not exist")

    def test_update_bucketlist_item(self):
        """
        Test API can edit a bucketlist item (PUT request)
        """
        data = json.dumps({
            "item_name":"Be A Python and Ruby Ninja(update)",
            "item_description":"Be a pro in flask, Django and Ruby on Rails"
        })

        # Make the post request and get the response
        response = self.app.put("/api/v1.0/bucketlists/1/items/1",
                                data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['Message'], "You have succesfully updated bucketlist item")

    def test_update_nonexisting_bucketlist_item(self):
        """
        Test API cannot update a bucketlist item that doesn't exist (PUT request)
        """
        data = json.dumps({
            "item_name":"Be A Python and Js Ninja",
            "item_description":"Be a pro in flask, Django, Angular, React and vue"
        })

        # Make the post request and get the response
        response = self.app.put("/api/v1.0/bucketlists/1/items/5778676",
                                data, content_type="application/json")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "bucketlist item does not exist")


    def test_can_delete_bucketlist_item(self):
        """
        Test API can delete an existing bucketlist (DELETE request)
        """
        response = self.app.delete("/api/v1.0/bucketlists/2")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "bucketlist item has been deleted")

    def test_delete_nonexistant_bucketlist_item(self):
        """
        Test API cannot delete a bucketlist item that does not exist (DELETE request)
        """
        response = self.app.delete("/api/v1.0/bucketlists/2")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "bucketlist item does not exist")

    def test_change_item_status_to_done(self):
        """
        Test API can change status of bucketlist item to done (PUT request)
        """
        data = json.dumps({
            "is_done": 1
        })

        # Make the post request and get the response
        response = self.app.put("/api/v1.0/bucketlists/1/items/2",
                                data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "item updated to done")

    def test_change_item_status_to_not_done(self):
        """
        Test API can change status a bucketlist item to not done (PUT request)
        """
        data = json.dumps({
            "is_done": 0
        })

        # Make the post request and get the response
        response = self.app.put("/api/v1.0/bucketlists/1/items/1",
                                data, content_type="application/json")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], "item updated to not done")
