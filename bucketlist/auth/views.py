import re
from flask.views import MethodView
from flask import make_response, request, jsonify
from bucketlist.models import User
from flask_cors import CORS, cross_origin
from . import auth_blueprint

class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view.r"""

        # Query to see if the user already exists
        user_email = User.query.filter_by(email=request.data['email']).first()
        user_username = User.query.filter_by(username=request.data['username']).first()

        if not user_email and not user_username:
            # There is no user so we'll try to register them
            try:
                # Register the user
                email = request.data['email']
                username = request.data['username']
                password = request.data['password']

                if not password:
                    response = {
                        'message': 'Missing Password.'
                    }
                     # return a response notifying the user password is missing
                    return make_response(jsonify(response)), 400

                if not username:
                    response = {
                        'message': 'Missing username.'
                    }
                     # return a response notifying the user that username are missing
                    return make_response(jsonify(response)), 400

                if not email:
                    response = {
                        'message': 'Missing email.'
                    }
                     # return a response notifying the user that email are missing
                    return make_response(jsonify(response)), 400
                
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

                if match is None:
                    response = {
                        'message': 'Sorry Invalid email. please put a valid email'
                    }
                     # return a response notifying the user that email is invalid
                    return make_response(jsonify(response)), 400

                check_username = re.match('^[a-zA-Z0-9_.-]+$', username)
                if check_username is None:
                    response = {
                        'message': 'Sorry Invalid Username format. please put a valid username'
                    }
                     # return a response notifying the user that credentials username is invalid
                    return make_response(jsonify(response)), 400

                user = User(username=username, email=email, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 409


class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view."""
        try:
            # Get the user object using their email (unique to every user)
            user = User.query.filter_by(email=request.data['email']).first()

            # Try to authenticate the found user using their password
            if user and user.password_is_valid(request.data['password']):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 400

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
# Define the rule for the registration url --->  api/v1.0/auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1.0/auth/register',
    view_func=registration_view,
    methods=['POST'])

# Define the rule for the registration url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1.0/auth/login',
    view_func=login_view,
    methods=['POST']
)
