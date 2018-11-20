import pyscopg2
from app.models.User import User
from app.models.Quotation import Quotation
from app.models.Parcel import Parcel


class Database():
	"""docstring for Database class"""
	__init__():
		connection = psycopg2.connect(user="postgres", password="", host="127.0.0.1", port="5432", database="send_it")
    	self.cursor = connection.cursor()
    	create_user_table()
    	create_parcel_table()
    	create_quotation_table()
   
    def create_user_table():
    	return cursor.execute("""IF NOT EXISTS CREATE TABLE users(
    							id INT PRIMARY KEY NOT NULL,
    							email TEXT NOT NULL,
    							password TEXT NOT NULL,
    							date_created TIMESTAMP NOT NULL,
    							date_modified TIMESTAMP NOT NULL)""");

    def create_parcel_table():
    	return cursor.execute("""IF NOT EXISTS CREATE TABLE parcels(
    							id INT PRIMARY KEY NOT NULL,
    							sender_id INT REFERENCES user(id),
    							status TEXT NOT NULL,
    							pick_up_address TEXT NOT NULL,
    							destination TEXT NOT NULL,
    							description TEXT NOT NULL,
    							sender_contact TEXT NOT NULL,
    							receiver_name TEXT NOT NULL,
    							receiver_contact TEXT NOT NULL,
    							size TEXT NOT NULL,
    							date_created TIMESTAMP NOT NULL,
    							date_modified TIMESTAMP NOT NULL)""")

    def create_quotation_table():
    	return cursor.execute("""IF NOT EXISTS CREATE TABLE quotations(
    							id INT PRIMARY KEY NOT NULL,
    							parcel_id INT REFERENCES parcels(id),
    							price TEXT NOT NULL,
    							parcel_items TEXT NOT NULL,
    							weight TEXT NOT NULL,
    							sender_id INT REFERENCES users(id),
    							receiver_name TEXT NOT NULL,
    							receiver_contact TEXT NOT NULL,
    							approx_delivery_duration TEXT NOT NULL,
    							prepared_by INT NOT NULL,
    							acceptance_status TEXT NOT NULL,
    							date_created TIMESTAMP NOT NULL,
    							date_modified TIMESTAMP NOT NULL);""")

    def get_all_users():
    	cursor.execute("SELECT * FROM users;")
    	users =  cursor.fetchall()
    	return users

    def get_all_parcels():
		postgreSQL_select_parcels_query = "SELECT * FROM parcels"
    	cursor.execute(postgreSQL_select_parcels_query)
    	parcels_records = cursor.fetchall()
    	return parcels_records

    def save_parcel(self, parcel):
    	postgres_insert_parcel_query = """ INSERT INTO parcels (id, sender_id, status, pick_up_address, destination,
    	description, sender_contact, receiver_name, receiver_contact, size) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		record_to_insert = (parcel.id, parcel.sender_id, parcel.status, parcel.pick_up_address, parcel.destination, parcel.description, parcel.sender_contact, parcel.receiver_name,parcel.receiver_contact, parcel.size)
		cursor.execute(postgres_insert_parcel_query, record_to_insert)
		connection.commit()

    def get_one_parcel(id):
    	sql_select_parcel_query = """SELECT * FROM parcels where id = %s"""
        cursor.execute(sql_select_parcel_query, (id))
        parcel = cursor.fetchone()
        return parcel

    def get_parcels_for_one_user(user_id):
    	sql_select_parcels_query = """SELECT * FROM parcels where sender_id = %s"""
        cursor.execute(sql_select_parcels_query, (user_id))
        parcel = cursor.fetchall()
        return parcel

    def change_status_of_parcel_cancel_delivery(parcel_id):
        sql_update_parcel_status_query = """UPDATE parcels SET status = %s WHERE id = %s"""
        cursor.execute(sql_update_query, ("Cancelled", parcel_id))
        connection.commit()

	def get_all_quotations():
		postgreSQL_select_quotations_Query = "SELECT * FROM quotations"
    	cursor.execute(postgreSQL_select_quotations_Query)
    	quotation_records = cursor.fetchall()
    	return quotation_records
   

	def save_quotation(self, quotation):
		postgres_insert_quotation_query = """ INSERT INTO quotations (id, parcel_id, price, parcel_items, weight, sender_id, receiver_name, receiver_contact, approx_delivery_duration, prepared_by, acceptance_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		record_to_insert = (quotation.id, quotation.parcel_id, quotation.price, quotation.parcel_items, quotation.weight, quotation.sender_id, quotation.receiver_name, quotation.receiver_contact, quotation.approx_delivery_duration, quotation.prepared_by, quotation.acceptance_status)
		cursor.execute(postgres_insert_quotation_query, record_to_insert)
		connection.commit()


    def get_one_quotation(id):
    	sql_select_quotation_query = """SELECT * FROM quotations where id = %s"""
        cursor.execute(sql_select_quotation_query, (id, ))
        quotation = cursor.fetchone()
        return quotation

    def get_quotations_for_one_user(user_id):
    	sql_select_quotations_query = """SELECT * FROM quotations where sender_id = %s"""
        cursor.execute(sql_select_quotations_query, (user_id, ))
        quotation = cursor.fetchall()
        return quotation

    def change_acceptance_status_of_quotation_cancel_delivery(quotation_id):
        sql_update_quotation_status_query = """UPDATE quotations SET acceptance_status = %s WHERE id = %s"""
        cursor.execute(sql_update_quotation_status_query, ("Cancelled", quotation_id))
        connection.commit()


    def save_new_user(self, user):
    	postgres_insert_user_query = """ INSERT INTO users (id, name, email, password) VALUES (%s,%s,%s,%s)"""
		record_to_insert = (user.id, user.name, user.email, user.password)
		cursor.execute(postgres_insert_user_query, record_to_insert)
		connection.commit()


    def get_registered_user(self, email, password):
    	sql_select_user_query = """SELECT * FROM users WHERE email = %s AND password = %s"""
        cursor.execute(sql_select_user_query, (email, password))
        user = cursor.fetchone()
        return user