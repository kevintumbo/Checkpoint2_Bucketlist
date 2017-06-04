from flask.ext.api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, jsonify, abort
# local import
from instance.config import app_config
from bucketlist import views

# This instance of a Blueprint that represents the authentication blueprint
auth_blueprint = Blueprint('auth', __name__)

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from bucketlist.models import Bucketlist

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/v1.0/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
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
                    bucketlist = Bucketlist(name=name)
                    bucketlist.save()
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'description': bucketlist.description,
                        'date_created': bucketlist.date_created,
                        'date_modifed': bucketlist.date_modifed,
                        'message': "You have succesfully created a bucketlist"
                    })
                    response.status_code = 201
                    return response
        else:
            # GET
            bucketlists = Bucketlist.get_all()
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
    return app

