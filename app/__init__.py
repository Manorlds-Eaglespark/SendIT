# app/__init__.py
"""File that has the routes for the api """
import os
import random
from flask_api import FlaskAPI
from flask import request, jsonify, make_response, abort
from app.models.User import User
from app.models.Parcel import Parcel
from app.models.Quotation import Quotation
from data_store.data import my_parcels, my_users, my_admins, my_quotations

# local import
from instance.config import app_config

def parcels_list(my_parcels):
	# GET all the parcels
    results = []
    for parcel in my_parcels:
        results.append(parcel)
    return results

def get_same_quotes(my_list, userz_id):
    lst = []
    for quote in my_quotations:
        if quote.sender_id == int(userz_id):
            lst.append(quote)
    return lst

def get_same(my_list, userz_id):
	lst = []
	for parcel in my_list:
		if parcel.sender_id == int(userz_id):
			lst.append(parcel)
	return lst

def soft_return(status, results):
	return make_response(jsonify({"status message": status, "meta": str(len(results)) + " items returned", "items": results})), 200

def my_item(parcel):
	return {
			'id': parcel.id,
	        'code': parcel.code,
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

def my_quote(quotation):
    return {
            "id": quotation.id,
            "parcel_code":quotation.parcel_code,
            "price":quotation.price,
            "parcel_items":quotation.parcel_items,
            "weight":quotation.weight,
            "sender_id":quotation.sender_id,
            "receiver_name":quotation.receiver_name,
            "receiver_contact":quotation.receiver_contact,
            "approx_delivery_duration":quotation.approx_delivery_duration,
            "prepared_by":quotation.prepared_by,
            "acceptance_status":quotation.acceptance_status
    }
def quote_response(quote, status):
    return {
        "status message":status,
        "item":my_quote(quote)
        }

def parcel_response(parcel, status):
	return {
		"status message":status,
        "item":my_item(parcel)
        }

def create_app(config_name):
    """Initialize the flask application"""
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')

#***************************************Fetch all parcel delivery orders & Make a new parcel delivery order

    @app.route('/v1/parcels', methods=['POST', 'GET'])
    def parcels():
        """fetch all orders or make an order"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                if request.method == "POST":

                    if not (request.data['sender_contact']):
                        return make_response(jsonify({"status message":"Please provide all the required details"})), 400

                    pcl_dict= {

                    "id" : len(my_parcels) + 1,
                    "code" : "i"+ str(random.randint(1000, 9999)),
                    "sender_id" : user_id,
                    "status" : "Initiated by Client",
                    "pick_up_address" : request.data['pick_up_address'],
                    "destination" : request.data['destination'],
                    "description" : request.data['description'],
                    "sender_contact" : request.data['sender_contact'],
                    "receiver_name" : request.data['receiver_name'],
                    "receiver_contact" : request.data['receiver_contact'],
                    "size" : request.data['size']
                    }

                    parcel = Parcel(pcl_dict)
                    my_parcels.append(parcel)       
                    response = jsonify({"status message":"New Delivery Order Successfully Added.", "item":my_item(parcel)})

                    return make_response(response), 201

                else:
                    # GET all the parcels
                    results = []
                    for parcel in my_parcels:
                        results.append(my_item(parcel))
                    return soft_return("All Parcel Delivery Orders", results)
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
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated
                correct_parcels = get_same(my_parcels, the_user_id)
                results = []

                for parcel in correct_parcels:
                        results.append(my_item(parcel))

                if len(results):
                    return soft_return("Success", results)
                    #return make_response(jsonify({"status message": "Success", "meta": str(len(results)) + " items returned", "items": results})), 200
                else:
                    return make_response(jsonify({"status message": "Fail- user has no orders or does not exist", "meta": str(len(results)) + " items returned"})), 404
              


#***************************************************************************Fetch a parcel delivery order

    @app.route('/v1/parcels/<int:id>', methods=['GET'])
    def my_parcel_with_id(id, **kwargs):
        """Fetch a specific parcel with its id"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                for prcl in my_parcels:
                    if prcl.id == id:
                        parcel = prcl
                        break
                else:
                    parcel = "Not there"

                if not isinstance(parcel, str):                    
                    if request.method == "GET":
                        return make_response(jsonify(parcel_response(parcel, "Success, item found"))), 200

                else:
                    return make_response(jsonify({"message":"Sorry, Parcel not found!"})), 404
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
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                for prcl in my_parcels:
                    if prcl.id == id:
                        parcel = prcl
                        break
                else:
                    parcel = "Not there"

                if not isinstance(parcel, str): 

                    if request.method == "PUT":
                        parcel.status = "Cancelled by Client"
                        return make_response(jsonify(parcel_response(my_parcels[parcel.id], 'Item Successfully Cancelled'))), 202

                else:
                    return make_response(jsonify({"message":"Sorry, Parcel not found!"})), 404
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401







#***************************************Fetch all and create quotations

    @app.route('/v1/quotations', methods=['POST', 'GET'])
    def quotations():
        """fetch all orders or make an order"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            user_email = User.decode_email(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated
                user = ""
                for userr in (my_admins + my_users):
                    if userr.email == user_email:
                        user = userr
                        break

                if user.is_admin:

                    if request.method == "POST":

                        if not (request.data['parcel_code']):
                            return make_response(jsonify({"status message":"A Parcel code is required."})), 400

                        qt_dict= {

                                    "id": len(my_quotations) + 1,
                                    "parcel_code":request.data["parcel_code"],
                                    "price":request.data["price"],
                                    "parcel_items":request.data["parcel_items"],
                                    "weight":request.data["weight"],
                                    "sender_id":request.data["sender_id"],
                                    "receiver_name":request.data["receiver_name"],
                                    "receiver_contact":request.data["receiver_contact"],
                                    "approx_delivery_duration":request.data["approx_delivery_duration"],
                                    "prepared_by":request.data["prepared_by"],
                                    "acceptance_status":request.data["acceptance_status"]
                                }

                        quote = Quotation(qt_dict)
                        my_quotations.append(quote)       
                        response = jsonify({"status message":"New Quotation Successfully created.", "item":my_quote(quote)})
                        return make_response(response), 201

                    else:
                        # GET all the parcels
                        results = []
                        for quotation in my_quotations:
                            results.append(my_quote(quotation))
                        return soft_return("All Quotations For All Orders", results)
                        #return make_response(jsonify({"status message":"All Parcel Delivery Orders", "meta": str(len(results))+" items returned","items":results})), 200
                else:
                    return make_response(jsonify({"status message":"Only Admins have access to this information."})), 400
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


#***************************************************************************Fetch a single quotation

    @app.route('/v1/quotations/<int:id>', methods=['GET'])
    def my_quotation_with_id(id, **kwargs):
        """Fetch a specific parcel with its id"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            user_email = User.decode_email(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated
                user = ""
                for userr in (my_admins + my_users):
                    if userr.email == user_email:
                        user = userr
                        break

                if user.is_admin:
                    for quote in my_quotations:
                        if quote.id == id:
                            quotation = quote
                            break
                    else:
                        quotation = "Not there"

                    if not isinstance(quotation, str):                    
                        if request.method == "GET":
                            return make_response(jsonify(quote_response(quotation, "Success, Quotation found"))), 200

                    else:
                        return make_response(jsonify({"message":"Sorry, Quotation not found!"})), 404
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401


#***************************************************************************Fetch all quotes to a specific user
    
    @app.route('/v1/users/<the_user_id>/quotations', methods=['GET'])
    def user_quotations(the_user_id, **kwargs):
        """Fetch order from one user"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated
                correct_quotes = get_same_quotes(my_quotations, the_user_id)
                results = []

                for quote in correct_quotes:
                        results.append(my_quote(quote))

                if len(results):
                    return soft_return("Success", results)
                    #return make_response(jsonify({"status message": "Success", "meta": str(len(results)) + " items returned", "items": results})), 200
                else:
                    return make_response(jsonify({"status message": "Fail- user has no orders or does not exist", "meta": str(len(results)) + " items returned"})), 404
              


#******************************************************************Order Sender Accepts Quote

    @app.route('/v1/quotations/<int:id>/user', methods=['PUT'])
    def accept_parcel_quotation(id, **kwargs):
        """Change the status of an order to canceled"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                for quote in my_quotations:
                    if quote.id == id:
                        user_quote = quote
                        break
                else:
                    user_quote = "Not there"

                if not isinstance(user_quote, str):
                    if user_quote.sender_id == user_id:
                        for prcl in my_parcels:
                            if prcl.code == user_quote.parcel_code:
                                parcel = prcl
                                break
                        else:
                            parcel = "Not there"

                        if not isinstance(parcel, str):
                            if request.method == "PUT":
                                user_quote.acceptance_status = "Accepted by user"
                                return make_response(jsonify(parcel_response(my_parcels[parcel.id], 'Item Successfully Cancelled'))), 202
                        else:
                            return make_response(jsonify({"status message":"Parcel for quotation not found."})), 404
                    else:
                        return make_response(jsonify({"status message":"Sorry, quotation for different user!"})), 404
                else:
                    return make_response(jsonify({"status message":"Sorry, Quotation not found!"})), 404
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