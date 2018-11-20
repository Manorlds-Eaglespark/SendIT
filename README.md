# SendIT   
[![Build Status](https://travis-ci.org/Manorlds-Eaglespark/SendIT.svg?branch=api)](https://travis-ci.org/Manorlds-Eaglespark/SendIT)  

[![Coverage Status](https://coveralls.io/repos/github/Manorlds-Eaglespark/SendIT/badge.svg?branch=api)](https://coveralls.io/github/Manorlds-Eaglespark/SendIT?branch=api)

<a href="https://codeclimate.com/github/Manorlds-Eaglespark/SendIT/maintainability"><img src="https://api.codeclimate.com/v1/badges/6e809a652b8b095e970b/maintainability" /></a>

SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories. 

# Business Logic
- When User comes, they login or register
- That User creates a parcel order for a delivery,
- Admin sees it and calls the client to confirm details, goes to pick-up them items, order status is *initiated by user*
- Admin weighs items, sends quote to client and who agrees, admin changes order status to *Active*, transports parcel.
- User can cancel or edit the order before it is with the stated recipient.*
- When parcel reaches recipient, client pays via Mobile money or Xente*, or Cash from recipeint.

# Roles
Admin Can:
		- send quote - update status_location(email notification) - request parcel recieved_confirmation
User Can:
		- create parcel, accept_quote, cancel_order, edit_order, confirm_goods_recieved

# User Interface Design
https://manorlds-eaglespark.github.io/SendIT/

# Hosted API
https://send-it-anorld-api.herokuapp.com

# Heroku API Endpoints
- GET v1/parcels       - Fetch all parcel delivery orders -> Admin

- GET v1/parcels/<parcelId>       - Fetch a specific parcel delivery order -> User
	
- GET v1/users/<userId>/parcels       - Fetch all parcel delivery orders by a specific user -> User
	
- PUT v1/parcels/<parcelId>/cancel       - Cancel the specific parcel delivery order -> User
	
- POST v1/parcels       - Create a parcel delivery order -> User

- POST v1/quotations      - Create a quotation for a client -> Admin

- GET v1/quotations       - Fetch all quotations -> Admin

- GET v1/quotations/<quoteId>       - Fetch a single quote -> User
	
- GET v1/users/<userId>/quotations       - Fetch quotes for a specific user -> User
	
- PUT v1/quotations/<userId>/user      - A clients accepts a quote from Admin  -> User

# Language
The application API is built on Python Flask micro api framework, hosted on Heroku. The UI is HTML, CSS and Javascript only.

# Setup Locally
You can clone this repo and use it on your machine, use this [link](https://github.com/Manorlds-Eaglespark/SendIT.git) to clone

# Author
Arnold Mukone
