# app/__init__.py
import re
from flask import Flask, request, jsonify, make_response, json
from datetime import datetime
from app.database.Database import Database
from instance.config import app_config

database = Database()

def create_app(config_name):

    from app.models.Parcel import Parcel
    from app.models.Quotation import Quotation
    from app.models.User import User

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')

    def get_access_token():
        """Get the access token from the header"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response(jsonify({"status message": "You have to login first."}))
        access_token = str(auth_header).split(" ")[1][:-1]
        return access_token

    @app.route('/api/v1/parcels', methods=['POST', 'GET'])
    def get_and_post_parcels():
        access_token = get_access_token()
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                if request.method == "POST":
                    pick_up_address = json.loads(request.data)['pick_up_address'],
                    destination = json.loads(request.data)['destination']
                    description = json.loads(request.data)['description']
                    sender_contact = json.loads(request.data)['sender_contact']
                    receiver_name = json.loads(request.data)['receiver_name']
                    receiver_contact = json.loads(request.data)['receiver_contact']
                    size = json.loads(request.data)['size']
                    if not isinstance(size, int):
                        return make_response(
                            jsonify({"message": "Please enter proper Kilogram size approximation as a number."})), 400
                    if not (pick_up_address and destination and description and sender_contact and
                            receiver_name and receiver_contact and size):
                        return make_response(jsonify({"message":"Please avail all the required details, and try again"})), 400
                    parcel_dict= {
                        "sender_id" : user_id,
                        "status" : "Initiated",
                        "pick_up_address" : pick_up_address,
                        "destination" : destination,
                        "current_location":pick_up_address,
                        "description" : description,
                        "sender_contact" : sender_contact,
                        "receiver_name" : receiver_name,
                        "receiver_contact" : receiver_contact,
                        "size" : size
                    }
                    parcel = Parcel(parcel_dict)
                    database.save_parcel(parcel)
                    the_added_parcel = database
                    parcel_item = {
                        'sender_id':parcel.sender_id,
                        'status':parcel.status,
                        'pick_up_address': parcel.pick_up_address[0],
                        'destination': parcel.destination,
                        'current_location':parcel.current_location[0],
                        'description': parcel.description,
                        'sender_contact': parcel.sender_contact,
                        'receiver_name': parcel.receiver_name,
                        'receiver_contact':parcel.receiver_contact,
                        'size':str(parcel.size) +" Kgs"
                        }
                    response = jsonify({"message":"New Delivery Order Successfully Added. Email sent to Admin.", "item":parcel_item})
                    return make_response(response), 201
                else:
                    admin_status = User.decode_admin_status(access_token)
                    if admin_status == "True":
                        parcels = database.get_all_parcels()
                        parcel_list = []
                        for parcel in parcels:
                            obj = {
                                    'id': parcel[0],
                                    'sender_id':parcel[1],
                                    'status':parcel[2],
                                    'pick_up_address': parcel[3],
                                    'destination': parcel[4],
                                    'current_location':parcel[5],
                                    'description': parcel[6],
                                    'sender_contact': parcel[7],
                                    'receiver_name': parcel[8],
                                    'receiver_contact':parcel[9],
                                    'size':str(parcel[10]) + " Kgs"
                                    }
                            parcel_list.append(obj)
                        return make_response(jsonify(parcel_list)), 200
                    else:
                        return make_response(jsonify({"message":"Sorry, you are not authorized to access this route."})), 403
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


    @app.route('/api/v1/users/<the_user_id>/parcels', methods=['GET'])
    def get_parcels_by_same_user(the_user_id):
        access_token = get_access_token()
        if access_token:
            user_id = User.decode_token(access_token)
            admin_status = User.decode_admin_status(access_token)
            if admin_status == "False":
                return make_response(jsonify({"message": "Sorry, you are not authorized to access this route."})), 403
            if not isinstance(user_id, str):
                parcels = database.get_parcels_for_one_user(the_user_id)
                parcel_list = []
                for parcel in parcels:
                        obj = {
                        'id': parcel[0],
                        'sender_id':parcel[1],
                        'status':parcel[2],
                        'pick_up_address': parcel[3],
                        'destination': parcel[4],
                        'current_location':parcel[5],
                        'description': parcel[6],
                        'sender_contact': parcel[7],
                        'receiver_name': parcel[8],
                        'receiver_contact':parcel[9],
                        'size':str(parcel[10])+" Kgs"
                        }
                        parcel_list.append(obj)
                if len(parcel_list):
                    return make_response(jsonify(parcel_list)), 200
                else:
                    return make_response(jsonify({"message": "User has no orders or does not exist"})), 404
              

    @app.route('/api/v1/parcels/<int:given_id>', methods=['GET'])
    def get_parcel_by_id(given_id):
        access_token = get_access_token()
        if access_token:
            user_id = User.decode_token(access_token)
            admin_status = User.decode_admin_status(access_token)
            if not isinstance(user_id, str):
                if request.method == "GET":
                    parcel = database.get_one_parcel(given_id)
                    if parcel[1] != user_id or admin_status == "False":
                        return make_response(jsonify({"message":"You need to be admin to view this info."})), 403
                    if not parcel:
                        return make_response(jsonify({"message":"Sorry, Parcel not found!"})), 404
                    else:                  
                            parcel_item = {
                            'id': parcel[0],
                            'sender_id':parcel[1],
                            'status':parcel[2],
                            'pick_up_address': parcel[3],
                            'destination': parcel[4],
                            'current_location':parcel[5],
                            'description': parcel[6],
                            'sender_contact': parcel[7],
                            'receiver_name': parcel[8],
                            'receiver_contact':parcel[9],
                            'size':str(parcel[10])+" Kgs"
                            }
                            return make_response(jsonify(parcel_item)), 200
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


    @app.route('/api/v1/parcels/<int:parcel_id>/cancel', methods=['PUT'])
    def cancel_my_parcel(parcel_id):
        access_token = get_access_token()
        if access_token:
            user_id = User.decode_token(access_token)
            admin_status = User.decode_admin_status(access_token)
            if not isinstance(user_id, str):
                if request.method == "PUT":
                    parcel = database.get_one_parcel(parcel_id)
                    if not parcel:
                        return make_response(jsonify({"message":"Parcel not found!"})), 404
                    else:
                        if parcel[1] != user_id or admin_status == "False":
                            return make_response(jsonify({"message": "You can only cancel a parcel you created"})), 400
                        database.change_status_of_parcel_cancel_delivery(parcel_id)
                        parcel = database.get_one_parcel(parcel_id)
                        parcel_item = {
                        'id': parcel[0],
                        'sender_id':parcel[1],
                        'status':parcel[2],
                        'pick_up_address': parcel[3],
                        'destination': parcel[4],
                        'current_location':parcel[5],
                        'description': parcel[6],
                        'sender_contact': parcel[7],
                        'receiver_name': parcel[8],
                        'receiver_contact':parcel[9],
                        'size':str(parcel[10])+" Kgs"
                        }
                        return make_response(jsonify(parcel_item)), 202
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/api/v1/parcels/<int:parcel_id>/destination', methods=['PUT'])
    def user_change_destination_parcel_address(parcel_id):
        access_token = get_access_token()
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                if request.method == "PUT":
                    new_parcel_address = json.loads(request.data)['new_address']
                    time_modified = datetime.now()
                    if re.search('[a-z]',new_parcel_address) is None or  len(new_parcel_address) < 5:
                        return make_response(jsonify({"message": "Use English alphabet and numbers. More than 5 chars long."})), 400
                    parcel = database.get_one_parcel(parcel_id)
                    if not parcel:
                        return make_response(jsonify({"message": "Parcel not found!"})), 404
                    else:
                        if parcel[2] == "Delivered":
                            return make_response(jsonify({"message": "Parcel was already delivered!"})), 400
                        if parcel[2] == "Cancelled":
                            return make_response(jsonify({"message": "You already cancelled this delivery"})), 400
                    if not parcel[1] == user_id:
                        return make_response(jsonify({"message":"You can only update parcel orders you made. Contact support immediately to clarify."})), 403
                    database.change_destination_of_parcel(parcel_id, new_parcel_address, time_modified)
                    parcel = database.get_one_parcel(parcel_id)
                    parcel_item = {
                        'id': parcel[0],
                        'sender_id': parcel[1],
                        'status': parcel[2],
                        'pick_up_address': parcel[3],
                        'destination': parcel[4],
                        'current_location': parcel[5],
                        'description': parcel[6],
                        'sender_contact': parcel[7],
                        'receiver_name': parcel[8],
                        'receiver_contact': parcel[9],
                        'size': str(parcel[10]) + " Kgs"
                    }
                    return make_response(jsonify(parcel_item)), 202
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/api/v1/parcels/<int:parcel_id>/status', methods=['PUT'])
    def admin_change_status_parcel_address(parcel_id):
        access_token = get_access_token()
        if access_token:
            user_id = User.decode_token(access_token)
            admin_status = User.decode_admin_status(access_token)
            if admin_status == "False":
                return make_response(jsonify({"message": "Sorry, you are not authorized to access this route!"})), 403
            if not isinstance(user_id, str):
                if request.method == "PUT":
                    new_status = json.loads(request.data)['status']
                    time_modified = datetime.now()
                    if not new_status.isalnum() and not new_status.isalpha() or len(new_status) < 3:
                        return make_response(jsonify(
                            {"message": "please use English alphabet. More than 3 chars long."})), 400
                    parcel = database.get_one_parcel(parcel_id)
                    if not parcel:
                        return make_response(jsonify({"message": "Parcel not found!"})), 404
                    else:
                        if parcel[2] == "Delivered":
                            return make_response(jsonify({"message": "Parcel already delivered! no longer be updated"})), 400
                        if parcel[2] == "Cancelled":
                            return make_response(
                                jsonify({"message": "User cancelled this delivery"})), 400
                    database.update_status_of_parcel(parcel_id, new_status, time_modified)
                    parcel = database.get_one_parcel(parcel_id)
                    parcel_item = {
                        'id': parcel[0],
                        'sender_id': parcel[1],
                        'status': parcel[2],
                        'pick_up_address': parcel[3],
                        'destination': parcel[4],
                        'current_location': parcel[5],
                        'description': parcel[6],
                        'sender_contact': parcel[7],
                        'receiver_name': parcel[8],
                        'receiver_contact': parcel[9],
                        'size': str(parcel[10]) + " Kgs"
                    }
                    return make_response(jsonify(parcel_item)), 202

            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401



    @app.route('/api/v1/parcels/<int:parcel_id>/presentLocation', methods=['PUT'])
    def admin_change_parcel_present_location(parcel_id):
        access_token = get_access_token()
        if access_token:
            user_id = User.decode_token(access_token)
            admin_status = User.decode_admin_status(access_token)
            if admin_status == "False":
                return make_response(jsonify({"message": "Sorry, you are not authorized to access this route!"})), 403
            if not isinstance(user_id, str):
                if request.method == "PUT":
                    current_location = json.loads(request.data)['location']
                    time_modified = datetime.now()
                    if not current_location.replace(" ", "").isalnum() and not current_location.replace("", " ").isalpha() or len(current_location) < 3:
                        return make_response(jsonify(
                            {"message": "please use only from the English alphabet. More than 3 chars long."})), 400
                    parcel = database.get_one_parcel(parcel_id)
                    if not parcel:
                        return make_response(jsonify({"message": "Parcel not found!"})), 404
                    else:
                        if parcel[2] == "Delivered":
                            return make_response(jsonify({"message": "Parcel already delivered! no longer be updated"})), 400
                        if parcel[2] == "Cancelled":
                            return make_response(
                                jsonify({"message": "User cancelled this delivery"})), 400
                    database.update_present_location_of_parcel(parcel_id, current_location, time_modified)
                    parcel = database.get_one_parcel(parcel_id)
                    parcel_item = {
                        'id': parcel[0],
                        'sender_id': parcel[1],
                        'status': parcel[2],
                        'pick_up_address': parcel[3],
                        'destination': parcel[4],
                        'current_location': parcel[5],
                        'description': parcel[6],
                        'sender_contact': parcel[7],
                        'receiver_name': parcel[8],
                        'receiver_contact': parcel[9],
                        'size': str(parcel[10]) + " Kgs"
                    }
                    return make_response(jsonify(parcel_item)), 202
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401



    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app