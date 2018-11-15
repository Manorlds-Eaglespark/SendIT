# SendIT   [![Build Status](https://travis-ci.org/Manorlds-Eaglespark/SendIT.svg?branch=api)](https://travis-ci.org/Manorlds-Eaglespark/SendIT)   [![Coverage Status](https://coveralls.io/repos/github/Manorlds-Eaglespark/SendIT/badge.svg?branch=api)](https://coveralls.io/github/Manorlds-Eaglespark/SendIT?branch=api)   <a href="https://codeclimate.com/github/Manorlds-Eaglespark/SendIT/maintainability"><img src="https://api.codeclimate.com/v1/badges/6e809a652b8b095e970b/maintainability" /></a>
SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories. 

# Business Logic Description
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

# User Interface Design Mockup
https://manorlds-eaglespark.github.io/SendIT/

# Hosted API (still being updated)
https://send-it-anorld-api.herokuapp.com

# Check the Pivotal Tracker Board to follow on the latest features to come
https://www.pivotaltracker.com/n/projects/2220223

# Repo Description
Sofar there have 5 branches

Main branch: Here will be the final code when the project is finally done
UI: This is the develop branch of the user interface
gh-pages: This is where the github pages can comfortably host the demo
api: This is where the API is taking shape that will power the whole application to life.
api_business: This is the develop branch of the api.


# Language
The application API is built on Python Flask micro api framework, hosted on Heroku. The UI is HTML, CSS and Javascript only.



# Author
Arnold Mukone
