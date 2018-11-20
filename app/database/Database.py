import psycopg2
from app.models.User import User
from app.models.Quotation import Quotation
from app.models.Parcel import Parcel


class Database():
    """docstring for Database class"""

    def __init__(self):
        self.connection = psycopg2.connect(user="postgres", password="", host="127.0.0.1", port="5432",
                                           database="send_it")
        self.cursor = self.connection.cursor()
        self.create_user_table()
        self.create_parcel_table()
        self.create_quotation_table()

    def create_user_table(self):
        sql_command = """CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY NOT NULL, email TEXT NOT NULL,
        password TEXT NOT NULL,
        date_created TIMESTAMP NOT NULL,
        date_modified TIMESTAMP NOT NULL)"""
        return self.cursor.execute(sql_command)

    def create_parcel_table(self):
        sql_command = """CREATE TABLE IF NOT EXISTS  parcels(
        id SERIAL PRIMARY KEY NOT NULL, sender_id INTEGER REFERENCES users(id),
        status TEXT NOT NULL,
        pick_up_address TEXT NOT NULL,
        destination TEXT NOT NULL,
        description TEXT NOT NULL,
        sender_contact TEXT NOT NULL,
        receiver_name TEXT NOT NULL,
        receiver_contact TEXT NOT NULL,
        size TEXT NOT NULL,
        date_created TIMESTAMP NOT NULL,
        date_modified TIMESTAMP NOT NULL)"""
        return self.cursor.execute(sql_command)

    def create_quotation_table(self):
        sql_command = """CREATE TABLE IF NOT EXISTS quotations(
        id SERIAL PRIMARY KEY NOT NULL, parcel_id INTEGER REFERENCES parcels(id),
        price TEXT NOT NULL,
        parcel_items TEXT NOT NULL,
        weight TEXT NOT NULL,
        sender_id INTEGER REFERENCES users(id),
        receiver_name TEXT NOT NULL,
        receiver_contact TEXT NOT NULL,
        approx_delivery_duration TEXT NOT NULL,
        prepared_by INT NOT NULL,
        acceptance_status TEXT NOT NULL,
        date_created TIMESTAMP NOT NULL,
        date_modified TIMESTAMP NOT NULL);"""
        return self.cursor.execute(sql_command)

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users;")
        users = self.cursor.fetchall()
        return users

    def get_all_parcels(self):
        postgresql_select_parcels_query = "SELECT * FROM parcels"
        self.cursor.execute(postgresql_select_parcels_query)
        parcels_records = self.cursor.fetchall()
        return parcels_records

    def save_parcel(self, parcel):
        postgres_insert_parcel_query = """ INSERT INTO parcels (id, sender_id, status, pick_up_address, destination,
        description, sender_contact, receiver_name, receiver_contact, size) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (
        parcel.id, parcel.sender_id, parcel.status, parcel.pick_up_address, parcel.destination, parcel.description,
        parcel.sender_contact, parcel.receiver_name, parcel.receiver_contact, parcel.size)
        self.cursor.execute(postgres_insert_parcel_query, record_to_insert)
        self.connection.commit()

    def get_one_parcel(self, id):
        sql_select_parcel_query = """SELECT * FROM parcels where id = %s"""
        self.cursor.execute(sql_select_parcel_query, (id))
        parcel = self.cursor.fetchone()
        return parcel

    def get_parcels_for_one_user(self,user_id):
        sql_select_parcels_query = """SELECT * FROM parcels where sender_id = %s"""
        self.cursor.execute(sql_select_parcels_query, (user_id,))
        parcel = self.cursor.fetchall()
        return parcel

    def change_status_of_parcel_cancel_delivery(self, parcel_id):
        sql_update_parcel_status_query = """UPDATE parcels SET status = %s WHERE id = %s"""
        self.cursor.execute(sql_update_parcel_status_query, ("Cancelled", parcel_id))
        self.connection.commit()

    def get_all_quotations(self):
        postgresql_select_quotations_query = "SELECT * FROM quotations"
        self.cursor.execute(postgresql_select_quotations_query)
        quotation_records = self.cursor.fetchall()
        return quotation_records

    def save_quotation(self, quotation):
        postgres_insert_quotation_query = """ INSERT INTO quotations (id, parcel_id, price, parcel_items, weight, sender_id, receiver_name, receiver_contact, approx_delivery_duration, prepared_by, acceptance_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (
        quotation.id, quotation.parcel_id, quotation.price, quotation.parcel_items, quotation.weight,
        quotation.sender_id, quotation.receiver_name, quotation.receiver_contact, quotation.approx_delivery_duration,
        quotation.prepared_by, quotation.acceptance_status)
        self.cursor.execute(postgres_insert_quotation_query, record_to_insert)
        self.connection.commit()

    def get_one_quotation(self, id):
        sql_select_quotation_query = """SELECT * FROM quotations where id = %s"""
        self.cursor.execute(sql_select_quotation_query, (id,))
        quotation = self.cursor.fetchone()
        return quotation

    def get_quotations_for_one_user(self, user_id):
        sql_select_quotations_query = """SELECT * FROM quotations where sender_id = %s"""
        self.cursor.execute(sql_select_quotations_query, (user_id,))
        quotation = self.cursor.fetchall()
        return quotation

    def change_acceptance_status_of_quotation_cancel_delivery(self, quotation_id):
        sql_update_quotation_status_query = """UPDATE quotations SET acceptance_status = %s WHERE id = %s"""
        self.cursor.execute(sql_update_quotation_status_query, ("Cancelled", quotation_id))
        self.connection.commit()

    def save_new_user(self, user):
        postgres_insert_user_query = """ INSERT INTO users (id, name, email, password) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (user.id, user.name, user.email, user.password)
        self.cursor.execute(postgres_insert_user_query, record_to_insert)
        self.connection.commit()

    def get_registered_user(self, email, password):
        sql_select_user_query = """SELECT * FROM users WHERE email = %s AND password = %s"""
        self.cursor.execute(sql_select_user_query, (email, password))
        user = self.cursor.fetchone()
        return user
