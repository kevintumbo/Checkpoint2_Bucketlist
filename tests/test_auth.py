import json
from tests.base_test import BaseTestCase

URL_Login = '/api/v1.0/auth/login'
URL_register =  '/api/v1.0/auth/register'


class TestAuthentication(BaseTestCase):
    """ Test cases for user registrstion, user authentication and log in"""

    def test_succesfull_user_registration(self):
        """
        Test API can succesfully a register a user
         (POST request)
        """

        data = json.dumps({
            "username": "maus",
            "email": "maus@gmail.com",
            "password": "deadmaus"
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "You have succesfully created a user")

    def test_user_registration_with_missing_username(self):
        """
        Test API cannot register a user if username is missing
         (POST request)
        """
        data = json.dumps({
            "username": " ",
            "email": "stan@gmail.com",
            "password": "stanbic"
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "username is missing")

    def test_user_registration_with_mising_email(self):
        """
        Test API cannot register a user if email is missing
         (POST request)
        """
        data = json.dumps({
            "username": "happy",
            "email": " ",
            "password": "wapi"
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Email address is missing")

    def test_user_registration_with_missing_password(self):
        """
        Test API cannot register a user if password is missing
         (POST request)
        """
        data = json.dumps({
            "username": "blackie",
            "email": "blackman@gmail.com",
            "password": " "
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Password is missing")

    def test_cannot_create_user_with_already_existing_email_address(self):
        """
        Test API cannot register a user if email address is already in the system
         (POST request)
        """
        data = json.dumps({
            "username": "snowpatrol",
            "email": "geo@gmail.com",
            "password": "openeyes"
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "email address already in use")

    def test_cannot_create_user_with_already_existing_username(self):
        """
        Test API cannot register a user if username is already in the system
         (POST request)
        """
        data = json.dumps({
            "username": "georgreen",
            "email": "redjump@gmail",
            "password": "heaven"
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "username already Taken")

    def test_succesfull_user_login(self):
        """
        Test API can sucesfully login a user (POST request)
        """

        data = json.dumps({
            "email": "ktumbo@gmail.com",
            "password": "password"
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Message'], "You have succesfully loggeg in")

    def test_user_login_with_missing_email(self):
        """
        Test API cannot log in a user if username is missing (POST request)
        """
        data = json.dumps({
            "email": " ",
            "password": "password"
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Email address is missing")

    def test_user_login_with_nonexisting_or_wrong_email_address(self):
        """
        Test API cannot log in a user if email address is wrong or does not exist
         (POST request)
        """
        data = json.dumps({
            "email": "kigumo@gmail.com",
            "password": "password"
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "wrong email/password combination")

    def test_user_login_with_missing_password(self):
        """
        Test API cannot log in a user if password is missing
         (POST request)
        """
        data = json.dumps({
            "email": "ktumbo@gmail.com",
            "password": " "
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Password is missing")

    def test_user_login_with_wrong_password(self):
        """
        Test API cannot log in a user if password is wrong
         (POST request)
        """
        data = json.dumps({
            "email": "ktumbo@gmail.com",
            "password": "atinini"
        })

        # Make the post request and get the response
        response = self.app.post(URL_register, data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "wrong email/password combination")
