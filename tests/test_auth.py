import json
from tests.base_test import BaseTestCase

URL_Login = '/api/v1.0/auth/login'
URL_register = '/api/v1.0/auth/register'


class TestAuthentication(BaseTestCase):
    """ Test cases for user registrstion, user authentication and log in"""

    def test_succesfull_user_registration(self):
        """
        Test API can succesfully a register a user
         (POST request)
        """

        self.data = {
            "username": "maus",
            "email": "maus@gmail.com",
            "password": "deadmaus"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("You registered successfully. Please log in.", str(response.data))

    def test_user_registration_with_missing_username(self):
        """
        Test API cannot register a user if username is missing
         (POST request)
        """
        self.data = {
            "username": "",
            "email": "stan@gmail.com",
            "password": "stanbic"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing username.", str(response.data))

    def test_user_registration_with_mising_email(self):
        """
        Test API cannot register a user if email is missing
         (POST request)
        """
        self.data = {
            "username": "happy",
            "email": "",
            "password": "wapi"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing email.", str(response.data))

    def test_user_registration_with_missing_password(self):
        """
        Test API cannot register a user if password is missing
         (POST request)
        """
        self.data = {
            "username": "blackie",
            "email": "blackman@gmail.com",
            "password": ""
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing Password", str(response.data))

    def test_cannot_create_user_with_already_existing_email_address(self):
        """
        Test API cannot register a user if email address is already in the system
         (POST request)
        """
        self.data = {
            "username": "snowpatrol",
            "email": "geo@gmail.com",
            "password": "openeyes"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)

        self.data = {
            "username": "werun",
            "email": "geo@gmail.com",
            "password": "foofighters"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)

        self.assertEqual(response.status_code, 409)
        self.assertIn("User already exists. Please login.", str(response.data))

    def test_cannot_create_user_with_already_existing_username(self):
        """
        Test API cannot register a user if username is already in the system
         (POST request)
        """
        self.data = {
            "username": "georgreen",
            "email": "redjump@gmail.com",
            "password": "heaven"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)

        self.data = {
            "username": "georgreen",
            "email": "geo@gmail.com",
            "password": "foofighters"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)

        self.assertEqual(response.status_code, 409)
        self.assertIn("User already exists. Please login.", str(response.data))
    
    def test_cannot_create_user_with_invalid_username(self):
        """
        Test API cannot register a user if username is invalid format
         (POST request)
        """
        self.data = {
            "username": ")()#%@#%@",
            "email": "redjump@gmail.com",
            "password": "heaven"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Sorry Invalid Username format. please put a valid username", str(response.data))

    def test_cannot_create_user_with_invalid_email(self):
        """
        Test API cannot register a user if email is invalid format
         (POST request)
        """
        self.data = {
            "username": "georgreen",
            "email": "redjump@gmail",
            "password": "heaven"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Sorry Invalid email. please put a valid email", str(response.data))

    def test_succesfull_user_login(self):
        """
        Test API can sucesfully login a user (POST request)
        """
        self.data = {
            "username": "georgreen",
            "email": "redjump@gmail.com",
            "password": "heaven"
        }

        # Make the post request and get the response
        response = self.client().post(URL_register, data=self.data)

        self.data = {
            "email": "redjump@gmail.com",
            "password": "heaven"
        }

        # Make the post request and get the response
        response = self.client().post(URL_Login, data=self.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("You logged in successfully.", str(response.data))

    def test_user_login_with_missing_email(self):
        """
        Test API cannot log in a user if username is missing (POST request)
        """
        self.data = {
            "email": " ",
            "password": "password"
        }

        # Make the post request and get the response
        response = self.client().post(URL_Login, data=self.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email or password, Please try again", str(response.data))


    def test_user_login_with_nonexisting_or_wrong_email_address(self):
        """
        Test API cannot log in a user if email address is wrong or does not exist
         (POST request)
        """
        self.data = {
            "email": "kigumo@gmail.com",
            "password": "password"
        }

        # Make the post request and get the response
        response = self.client().post(URL_Login, data=self.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email or password, Please try again", str(response.data))

    def test_user_login_with_missing_password(self):
        """
        Test API cannot log in a user if password is missing
         (POST request)
        """
        self.data = {
            "email": "ktumbo@gmail.com",
            "password": ""
        }

        # Make the post request and get the response
        response = self.client().post(URL_Login, data=self.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email or password, Please try again", str(response.data))

    def test_user_login_with_wrong_password(self):
        """
        Test API cannot log in a user if password is wrong
         (POST request)
        """
        self.data = {
            "email": "ktumbo@gmail.com",
            "password": "atinini"
        }

        # Make the post request and get the response
        response = self.client().post(URL_Login, data=self.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email or password, Please try again", str(response.data))
