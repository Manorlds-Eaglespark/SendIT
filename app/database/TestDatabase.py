import psycopg2


class TestDatabase:
	"""docstring for Test Database class"""

	def __init__(self):
		self.connection = psycopg2.connect(user="postgres", password="", host="127.0.0.1", port="5432",
										   database="test_db")
		self.cursor = self.connection.cursor()
		self.connection.autocommit = True

	def create_all_tables(self):
		#create all database tables for test purposes

		sql_command_users_table = ("CREATE TABLE users"
					   "(id SERIAL PRIMARY KEY, name TEXT NOT NULL,"
					   "email TEXT NOT NULL,"
					   "password TEXT NOT NULL,"
					   "is_admin TEXT NOT NULL,"
					   "date_created TIMESTAMP NOT NULL,"
					   "date_modified TIMESTAMP NOT NULL)")

		sql_command_parcels_table = ("CREATE TABLE parcels"
					   "(id SERIAL PRIMARY KEY,"
					   "sender_id INTEGER REFERENCES users(id),"
					   "status TEXT NOT NULL,"
					   "pick_up_address TEXT NOT NULL,"
					   "destination TEXT NOT NULL,"
					   "description TEXT NOT NULL,"
					   "sender_contact TEXT NOT NULL,"
					   "receiver_name TEXT NOT NULL,"
					   "receiver_contact TEXT NOT NULL,"
					   "size TEXT NOT NULL,"
					   "date_created TIMESTAMP NOT NULL,"
					   "date_modified TIMESTAMP NOT NULL)")

		sql_command_quotations_table = ("CREATE TABLE quotations"
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
		sql_command_users_table = "DROP TABLE users"
		sql_command_parcels_table = "DROP TABLE parcels"
		sql_command_quotations_table = "DROP TABLE quotations"

		self.cursor.execute(sql_command_users_table)
		self.cursor.execute(sql_command_parcels_table)
		self.cursor.execute(sql_command_quotations_table)