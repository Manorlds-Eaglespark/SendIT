import psycopg2
import os
from app.data_store.data import admin_data
from app.models.Admin import Admin
class Database:
    """docstring for Database class"""

    def __init__(self):
        db_name = os.getenv("DATABASE")
        self.connection = psycopg2.connect(user="wlovhtswtdroli", password="de5b58a980ee9fd04b435b4b95634a58a5968e330b41da3ae2bb611dd7a6b881", host="ec2-50-19-249-121.compute-1.amazonaws.com", port="5432",
                                           database="d79qu8i9e3hqlv")
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True
        self.admin = Admin(admin_data)
        self.database.save_new_user(self.admin)

    def create_user_table(self):
        """create a user table"""
        sql_command = ("CREATE TABLE IF NOT EXISTS users"
                       "(id SERIAL PRIMARY KEY, name TEXT NOT NULL,"
                       "email TEXT NOT NULL,"
                       "password TEXT NOT NULL,"
                       "is_admin TEXT NOT NULL,"
                       "date_created TIMESTAMP NOT NULL,"
                       "date_modified TIMESTAMP NOT NULL)")
        self.cursor.execute(sql_command)

    def create_parcel_table(self):
        """create a parcels table"""
        sql_command = ("CREATE TABLE IF NOT EXISTS  parcels"
                       "(id SERIAL PRIMARY KEY,"
                       "sender_id INTEGER REFERENCES users(id),"
                       "status TEXT NOT NULL,"
                       "pick_up_address TEXT NOT NULL,"
                       "destination TEXT NOT NULL,"
                       "current_location TEXT NOT NULL,"
                       "description TEXT NOT NULL,"
                       "sender_contact TEXT NOT NULL,"
                       "receiver_name TEXT NOT NULL,"
                       "receiver_contact TEXT NOT NULL,"
                       "size TEXT NOT NULL,"
                       "date_created TIMESTAMP NOT NULL,"
                       "date_modified TIMESTAMP NOT NULL)")
        self.cursor.execute(sql_command)

    def create_quotation_table(self):
        """create a quotations table"""
        sql_command = ("CREATE TABLE IF NOT EXISTS quotations"
                       "(id SERIAL PRIMARY KEY NOT NULL, parcel_id INTEGER REFERENCES parcels(id),"
                       "price TEXT NOT NULL,"
                       "parcel_items TEXT NOT NULL,"
                       "weight TEXT NOT NULL,"
                       "sender_id INTEGER REFERENCES users(id),"
                       "receiver_name TEXT NOT NULL,"
                       "receiver_contact TEXT NOT NULL,"
                       "approx_delivery_duration TEXT NOT NULL,"
                       "prepared_by INT NOT NULL,"
                       "acceptance_status TEXT NOT NULL,"
                       "date_created TIMESTAMP NOT NULL,"
                       "date_modified TIMESTAMP NOT NULL);")
        self.cursor.execute(sql_command)

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users;")
        users = self.cursor.fetchall()
        return users

    def get_like_this_in_database(self, parcel_date_created):
        postgresql_select_parcels_query = "SELECT * FROM parcels where date_created = %s"
        self.cursor.execute(postgresql_select_parcels_query, (parcel_date_created,))
        parcel = self.cursor.fetchone()
        return parcel

    def get_all_parcels(self):
        """get all the parcels in the database"""
        postgresql_select_parcels_query = "SELECT * FROM parcels"
        self.cursor.execute(postgresql_select_parcels_query)
        parcels_records = self.cursor.fetchall()
        return parcels_records

    def save_parcel(self, parcel):
        postgres_insert_parcel_query = ("INSERT INTO parcels ("
        "sender_id, status, pick_up_address, destination, current_location,"
    "description, sender_contact, receiver_name, receiver_contact, size, date_created, date_modified) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        record_to_insert = (
            parcel.sender_id, parcel.status, parcel.pick_up_address, parcel.destination, parcel.current_location, parcel.description,
            parcel.sender_contact, parcel.receiver_name, parcel.receiver_contact, parcel.size, parcel.date_created,
            parcel.date_modified)
        self.cursor.execute(postgres_insert_parcel_query, record_to_insert)

    def get_one_parcel(self, parcel_id):
        """returns a parcel row given the parcel id"""
        sql_select_parcel_query = """SELECT * FROM parcels where id = %s"""
        self.cursor.execute(sql_select_parcel_query, (parcel_id,))
        parcel = self.cursor.fetchone()
        return parcel

    def get_parcels_for_one_user(self, user_id):
        """Get parcels of one user"""
        sql_select_parcels_query = """SELECT * FROM parcels where sender_id = %s"""
        self.cursor.execute(sql_select_parcels_query, (user_id,))
        parcel = self.cursor.fetchall()
        return parcel

    def change_destination_of_parcel(self, parcel_id, destination, date_modified):
        sql_update_parcel_destination_query = """UPDATE parcels SET destination = %s, date_modified = %s WHERE id = %s"""
        self.cursor.execute(sql_update_parcel_destination_query, (destination, date_modified, parcel_id))

    def update_status_of_parcel(self, parcel_id, status, date_modified):
        sql_update_parcel_status_query = """UPDATE parcels SET status = %s, date_modified = %s WHERE id = %s"""
        self.cursor.execute(sql_update_parcel_status_query, (status, date_modified, parcel_id))

    def update_present_location_of_parcel(self, parcel_id, location, date_modified):
        sql_update_parcel_status_query = """UPDATE parcels SET current_location = %s, date_modified = %s WHERE id = %s"""
        self.cursor.execute(sql_update_parcel_status_query, (location, date_modified, parcel_id))

    def change_status_of_parcel_cancel_delivery(self, parcel_id):
        sql_update_parcel_status_query = """UPDATE parcels SET status = %s WHERE id = %s"""
        self.cursor.execute(sql_update_parcel_status_query, ("Cancelled", parcel_id))

    def make_admin(self, user_id):
        sql_update_user_status_query = """UPDATE users SET is_admin = %s WHERE id = %s"""
        self.cursor.execute(sql_update_user_status_query, ("True", user_id))

    def get_a_user(self, user_id):
        sql_user_query = """SELECT * FROM users WHERE id = %s"""
        self.cursor.execute(sql_user_query, (user_id,))
        user = self.cursor.fetchone()
        return user

    def get_id_given_email(self, email):
        sql_user_query = """SELECT id FROM users WHERE email = %s"""
        self.cursor.execute(sql_user_query, (email,))
        the_id = self.cursor.fetchone()
        return the_id

    def save_new_user(self, user):
        """save a new user to the database"""
        postgres_insert_user_query = """ INSERT INTO users (name, email, password, is_admin, date_created, date_modified) VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (user.name, user.email, user.password, user.is_admin, user.date_created, user.date_modified)
        self.cursor.execute(postgres_insert_user_query, record_to_insert)

    def get_registered_user(self, email):
        sql_select_user_query = """SELECT * FROM users WHERE email = %s"""
        self.cursor.execute(sql_select_user_query, (email,))
        user = self.cursor.fetchone()
        return user

    def create_all_tables(self):
        sql_command_users_table = ("CREATE TABLE IF NOT EXISTS users"
                                   "(id SERIAL PRIMARY KEY, name TEXT NOT NULL,"
                                   "email TEXT NOT NULL,"
                                   "password TEXT NOT NULL,"
                                   "is_admin TEXT NOT NULL,"
                                   "date_created TIMESTAMP NOT NULL,"
                                   "date_modified TIMESTAMP NOT NULL)")

        sql_command_parcels_table = ("CREATE TABLE IF NOT EXISTS parcels"
                                     "(id SERIAL PRIMARY KEY,"
                                     "sender_id INTEGER REFERENCES users(id),"
                                     "status TEXT NOT NULL,"
                                     "pick_up_address TEXT NOT NULL,"
                                     "destination TEXT NOT NULL,"
                                     "current_location TEXT NOT NULL,"
                                     "description TEXT NOT NULL,"
                                     "sender_contact TEXT NOT NULL,"
                                     "receiver_name TEXT NOT NULL,"
                                     "receiver_contact TEXT NOT NULL,"
                                     "size INTEGER NOT NULL,"
                                     "date_created TIMESTAMP NOT NULL,"
                                     "date_modified TIMESTAMP NOT NULL)")

        sql_command_quotations_table = ("CREATE TABLE IF NOT EXISTS quotations"
                                        "(id SERIAL PRIMARY KEY NOT NULL, parcel_id INTEGER REFERENCES parcels(id),"
                                        "price TEXT NOT NULL,"
                                        "parcel_items TEXT NOT NULL,"
                                        "weight TEXT NOT NULL,"
                                        "sender_id INTEGER REFERENCES users(id),"
                                        "receiver_name TEXT NOT NULL,"
                                        "receiver_contact TEXT NOT NULL,"
                                        "approx_delivery_duration TEXT NOT NULL,"
                                        "prepared_by INT NOT NULL,"
                                        "acceptance_status TEXT NOT NULL,"
                                        "date_created TIMESTAMP NOT NULL,"
                                        "date_modified TIMESTAMP NOT NULL);")

        self.cursor.execute(sql_command_users_table)
        self.cursor.execute(sql_command_parcels_table)
        self.cursor.execute(sql_command_quotations_table)

    def delete_all_tables(self):
        sql_delete_command_users_table = "TRUNCATE TABLE users RESTART IDENTITY CASCADE"
        sql__delete_command_parcels_table = "TRUNCATE TABLE parcels RESTART IDENTITY CASCADE"
        sql_delete_command_quotations_table = "TRUNCATE TABLE quotations RESTART IDENTITY CASCADE"

        self.cursor.execute(sql_delete_command_users_table)
        self.cursor.execute(sql__delete_command_parcels_table)
        self.cursor.execute(sql_delete_command_quotations_table)
