import os
from app import create_app

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)

from app.database import Database

database = Database()
database.create_user_table()

if __name__ == '__main__':  
    app.run()