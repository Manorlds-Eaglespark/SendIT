import os
from app import create_app
from app.models.Admin import Admin
from app.data_store.data import admin_data

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)

from app.database.Database import Database

database = Database()
database.create_all_tables()
database.delete_all_tables()
admin = Admin(admin_data)
database.save_new_user(admin)

if __name__ == '__main__':  
    app.run()