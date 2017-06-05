from flask.ext.api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, jsonify, abort
# local import
from instance.config import app_config

# This instance of a Blueprint that represents the authentication blueprint
auth_blueprint = Blueprint('auth', __name__)

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from bucketlist.models import Bucketlist, Item, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/v1.0/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
             # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated
                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    description = str(request.data.get('description', ''))

                    if not name:
                        response = jsonify({
                            'message': "bucketlist missing name"
                        })
                        response.status_code = 400
                        return response
                    if not description:
                        response = jsonify({
                            'message': "Bucketlist desscription missing"
                        })
                        response.status_code = 400
                        return response
                    if name:
                        check_bucketlist = Bucketlist.query.filter_by(name=name).first()
                        if check_bucketlist:
                            response = jsonify({
                                'message': "That bucketlist already exists"
                            })
                            response.status_code = 409
                            return response
                        else:
                            bucketlist = Bucketlist(name=name, description=description,
                                                    owner_id=user_id)
                            bucketlist.save()
                            response = jsonify({
                                'id': bucketlist.id,
                                'name': bucketlist.name,
                                'description': bucketlist.description,
                                'owner_id':bucketlist.owner_id,
                                'date_created': bucketlist.date_created,
                                'date_modifed': bucketlist.date_modifed,
                                'message': "You have succesfully created a bucketlist"
                            })
                            response.status_code = 201
                            return response
                else:
                    # GET
                    bucketlists = Bucketlist.query.filter_by(owner_id=user_id)
                    results = []

                    for bucketlist in bucketlists:
                        obj = {
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified
                        }
                        results.append(obj)
                    response = jsonify(results)
                    response.status_code = 200
                    return response
            else:
                response = jsonify({
                    'message': "Invalid Token"
                })
                response.status_code = 401
                return response
    @app.route('/api/v1.0/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id):
     # retrieve a buckelist using it's ID
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
                "message": "bucketlist {} deleted successfully".format(bucketlist.id)
            }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modifed': bucketlist.date_modifed,
                'message':"You have succesfully updated a bucketlist"
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modifed': bucketlist.date_modifed
            })
            response.status_code = 200
            return response

    @app.route('/api/v1.0/bucketlists/<int:id>/items/', methods=['POST'])
    def bucketlists_items(id):
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
             # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated
                if request.method == "POST":

                    bucketlist = Bucketlist.query.filter_by(id=id).first()
                    if not bucketlist:
                        response = jsonify({
                            'message': "Bucketlist does not exist"
                            })
                        response.status_code = 404
                        return response
                    else:
                        name = str(request.data.get('item_name', ''))
                        description = str(request.data.get('item_description', ''))
                        if not name:
                            response = jsonify({
                                'message': "bucketlist item missing name"
                            })
                            response.status_code = 400
                            return response
                        if not description:
                            response = jsonify({
                                'message': "Bucketlist item description missing"
                            })
                            response.status_code = 400
                            return response

                        get_owner_items = Item.query.filter_by(owner_id=user_id,
                                                               item_name=name).first()
                        if get_owner_items:
                            response = jsonify({
                                'message': "That bucketlist item already exists"
                            })
                            response.status_code = 409
                            return response

                        else:
                            item = Item(item_name=name, item_description=description,
                                        owner_id=user_id, bucketlist_id=id)
                            item.save()
                            response = jsonify({
                                'id': item.id,
                                'name': item.item_name,
                                'description': item.item_description,
                                'is_done':item.is_done,
                                'bucketlist_id':item.bucketlist_id,
                                'owner_id':item.owner_id,
                                'date_modified': item.date_modified,
                                'message': "You have succesfully created a bucketlist item"
                            })
                            response.status_code = 201
                            return response

    @app.route('/api/v1.0/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
    def bucketlist_items_manipulation(id, item_id):
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
             # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated
                # retrieve a buckelist using it's ID
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    response = jsonify({
                        'message': "Bucketlist does not exist"
                        })
                    response.status_code = 404
                    return response

                if request.method == 'DELETE':
                    item = Item.query.filter_by(bucketlist_id=id,
                                                id=item_id, owner_id=user_id).first()
                    if not item:
                        response = jsonify({
                            'message': "Bucketlist item does not exist"
                        })
                        response.status_code = 404
                        return response
                    else:
                        item.delete()
                        return {
                            "message": "bucketlist item {} deleted successfully".format(item.id)
                        }, 200

                if request.method == 'PUT':
                    item = Item.query.filter_by(bucketlist_id=id,
                                                id=item_id, owner_id=user_id).first()
                    if not item:
                        response = jsonify({
                            'message': "Bucketlist item does not exist"
                        })
                        response.status_code = 404
                        return response
                    else:
                        name = str(request.data.get('item_name', ''))
                        description = str(request.data.get('item_description', ''))
                        done = str(request.data.get('is_done', ''))
                        item.item_name = name
                        item.item_description = description
                        item.is_done = done
                        item.save()
                        response = jsonify({
                            'id': item.id,
                            'name': item.item_name,
                            'description': item.item_description,
                            'is_done':item.is_done,
                            'bucketlist_id':item.bucketlist_id,
                            'owner_id':item.owner_id,
                            'date_modified': item.date_modified,
                            'message':"You have succesfully updated a bucketlist item"
                        })
                        response.status_code = 200
                        return response
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app

