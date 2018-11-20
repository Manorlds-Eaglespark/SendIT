# app/__init__.py
from flask import request, jsonify, make_response, abort

import os

# local import
from instance.config import app_config


def create_app(config_name):

    from app.models.Parcel import Parcel
    from app.models.Quotation import Quotation
    from app.models.User import User


    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')

    def get_access_token():
        """Get the access token from the header"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response(jsonify({"status message": "You have to login first."}))
        access_token = str(auth_header).split(" ")[1][:-1]
        return access_token


#***************************************Fetch all parcel delivery orders & Make a new parcel delivery order

    @app.route('/v1/parcels', methods=['POST', 'GET'])
    def parcels():
        """fetch all orders or make an order"""


        access_token = get_access_token()
        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                if request.method == "POST":

                    pick_up_address = request.data['pick_up_address'], 
                    destination = request.data['destination']
                    description = request.data['description']
                    sender_contact = request.data['sender_contact']
                    receiver_name = request.data['receiver_name']
                    receiver_contact = request.data['receiver_contact']
                    size = request.data['size']

                    if not (pick_up_address and destination and description and sender_contact and receiver_name and receiver_contact and size):
                        return make_response(jsonify({"status message":"Please avail all the required details, and try again"})), 400

                    pcl_dict= {
                    "sender_id" : user_id,
                    "status" : "Initiated",
                    "pick_up_address" : request.data['pick_up_address'],
                    "destination" : request.data['destination'],
                    "description" : request.data['description'],
                    "sender_contact" : request.data['sender_contact'],
                    "receiver_name" : request.data['receiver_name'],
                    "receiver_contact" : request.data['receiver_contact'],
                    "size" : request.data['size']
                    }

                    parcel = Parcel(pcl_dict)
                    ####save parcel here
                    parcel_item = {
                        'id': parcel.id,
                        'sender_id':parcel.sender_id,
                        'status':parcel.status,
                        'pick_up_address': parcel.pick_up_address,
                        'destination': parcel.destination,
                        'description': parcel.description,
                        'sender_contact': parcel.sender_contact,
                        'receiver_name': parcel.receiver_name,
                        'receiver_contact':parcel.receiver_contact,
                        'size':parcel.size 
                        }
                    response = jsonify({"status message":"New Delivery Order Successfully Added. Email sent to Admin.", "item":parcel_item})

                    return make_response(response), 201

                else:
                    # GET all the parcels
                    parcels = #get parcels from database
                    results = []

                    for parcel in parcels:
                        obj = {
                        'id': parcel.id,
                        'sender_id':parcel.sender_id,
                        'status':parcel.status,
                        'pick_up_address': parcel.pick_up_address,
                        'destination': parcel.destination,
                        'description': parcel.description,
                        'sender_contact': parcel.sender_contact,
                        'receiver_name': parcel.receiver_name,
                        'receiver_contact':parcel.receiver_contact,
                        'size':parcel.size 
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
                    #return make_response(jsonify({"status message":"All Parcel Delivery Orders", "meta": str(len(results))+" items returned","items":results})), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401



#***************************************************************************Fetch all parcel delivery orders by a specific user
    @app.route('/v1/users/<the_user_id>/parcels', methods=['GET'])
    def user_parcels(the_user_id, **kwargs):
        """Fetch order from one user"""

        access_token = get_access_token()
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated
                parcels = #get parcels for one user from database
                results = []

                for parcel in parcels:
                        obj = {
                        'id': parcel.id,
                        'sender_id':parcel.sender_id,
                        'status':parcel.status,
                        'pick_up_address': parcel.pick_up_address,
                        'destination': parcel.destination,
                        'description': parcel.description,
                        'sender_contact': parcel.sender_contact,
                        'receiver_name': parcel.receiver_name,
                        'receiver_contact':parcel.receiver_contact,
                        'size':parcel.size 
                        }
                        results.append(obj)

                if len(results):
                    return make_response(jsonify(results)), 200
                    #return make_response(jsonify({"status message": "Success", "meta": str(len(results)) + " items returned", "items": results})), 200
                else:
                    return make_response(jsonify({"status message": "User has no orders or does not exist", "meta": str(len(results)) + " items returned"})), 404
              

#***************************************************************************Fetch a parcel delivery order

    @app.route('/v1/parcels/<int:id>', methods=['GET'])
    def my_parcel_with_id(id, **kwargs):
        """Fetch a specific parcel with its id"""
        
        access_token = get_access_token()
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                if request.method == "GET":

                    parcel = #get the parcel from the database

                    if not parcel:
                        return make_response(jsonify({"message":"Sorry, Parcel not found!"})), 404 
                    else:                  
                            parcel_item = {
                            'id': parcel.id,
                            'sender_id':parcel.sender_id,
                            'status':parcel.status,
                            'pick_up_address': parcel.pick_up_address,
                            'destination': parcel.destination,
                            'description': parcel.description,
                            'sender_contact': parcel.sender_contact,
                            'receiver_name': parcel.receiver_name,
                            'receiver_contact':parcel.receiver_contact,
                            'size':parcel.size 
                            }
                            return make_response(jsonify(parcel_item)), 200
                        
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401


#***************************************************************************Cancel a parcel delivery order

    @app.route('/v1/parcels/<int:id>/cancel', methods=['PUT'])
    def cancel_my_parcel(id, **kwargs):
        """Change the status of an order to canceled"""

        access_token = get_access_token()
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                if request.method == "PUT":
                    parcel = #get the parcel to update
                    if not parcel:
                        return make_response(jsonify({"message":"Parcel not found!"})), 404
                    else:
                            parcel.status = "Cancelled"
                            parcel.save()
                            parcel_item = {
                            'id': parcel.id,
                            'sender_id':parcel.sender_id,
                            'status':parcel.status,
                            'pick_up_address': parcel.pick_up_address,
                            'destination': parcel.destination,
                            'description': parcel.description,
                            'sender_contact': parcel.sender_contact,
                            'receiver_name': parcel.receiver_name,
                            'receiver_contact':parcel.receiver_contact,
                            'size':parcel.size 
                            }
                            return make_response(jsonify(parcel_item)), 202

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401




    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app