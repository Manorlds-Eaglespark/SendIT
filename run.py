import os
from app import create_app

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)

from app.database.Database import Database

database = Database()
database.create_user_table()
database.create_parcel_table()
database.create_quotation_table()

if __name__ == '__main__':  
    app.run()