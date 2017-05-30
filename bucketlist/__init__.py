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
            if name:
                bucketlist = Bucketlist(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
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

    @app.route('/bucketlists/<int:id>', methods=['POST','GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
           #########################################################
        ### Existing code for creating, updating and deleting a bucketlist #####
        #########################################################

        app.register_blueprint(auth_blueprint)
    return app

