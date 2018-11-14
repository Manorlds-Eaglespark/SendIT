
from app.models import *


initDict1 = {"id":1,
			"code":"i5261",
			"sender_id":1,
			"status":"Delivered",
			"pick_up_address":"Ssebagala stage, Kisasi",
			"destination":"Namakwekwe, Mbale",
			"description":"2 CMA books",
			"sender_contact":"0757877585",
			"receiver_name":"Kitebe John",
			"receiver_contact":"0772449361",
			"size":"Small Parcel: Documents, Envelope items. less than 20KGs"}

initDict2 = {"id":2,
			"code":"i5659",
			"sender_id":2,
			"status":"Initiated by Client",
			"pick_up_address":"Garden City, 1st gate down from Jinja road",
			"destination":"Garden City, 2nd Level, Shop 32",
			"description":"Women Jewellery",
			"sender_contact":"0757877585",
			"receiver_name":"Zimulati Nagudi",
			"receiver_contact":"0782203860",
			"size":"Medium Parcel: less than 65KGs"}


initDict3 = {"id":3,
			"code":"i2562",
			"sender_id":1,
			"status":"Active",
			"pick_up_address":"Ssebagala stage, Kisasi",
			"destination":"Shell gas station, Kamwokya",
			"description":"Gas Cannister",
			"sender_contact":"0757877585",
			"receiver_name":"Amos Lwegela",
			"receiver_contact":"075256656",
			"size":"Small Parcel: Documents, Envelope items. less than 20KGs"}


initDict4 = {"id":4,
			"code":"i2562",
			"sender_id":3,
			"status":"Initiated by Client",
			"pick_up_address":"Boulevard, Kampala road, shop D52",
			"destination":"Ssebagala stage, Kisasi",
			"description":"New Nokia 8",
			"sender_contact":"0775225525",
			"receiver_name":"Anorld Mukone",
			"receiver_contact":"0757877585",
			"size":"Small Parcel: Documents, Envelope items. less than 20KGs"}


initDict5 = {"id":5,
			"code":"i2531",
			"sender_id":2,
			"status":"Delivered",
			"pick_up_address":"Garden City, 1st gate down from Jinja road",
			"destination":"Ssebagala stage, Kisasi",
			"description":"Space Cookies",
			"sender_contact":"077256555",
			"receiver_name":"Anorld Mukone",
			"receiver_contact":"0757877585",
			"size":"Small Parcel: Documents, Envelope items. less than 20KGs"}


initDict6 = {"id":6,
			"code":"i5426",
			"sender_id":1,
			"status":"Active",
			"pick_up_address":"Ssebagala stage, Kisasi",
			"destination":"Banda stage, Jinja road",
			"description":"Sauce pans",
			"sender_contact":"0757877585",
			"receiver_name":"Emma Richard",
			"receiver_contact":"0705256546",
			"size":"Medium Parcel: less than 65KGs"}


initDict7 = {"id":7,
			"code":"i5565",
			"sender_id":1,
			"status":"Initiated by Client",
			"pick_up_address":"Ssebagala stage, Kisasi",
			"destination":"Banda stage, Jinja road",
			"description":"Need 4 speed cd",
			"sender_contact":"0757877585",
			"receiver_name":"Ian Kendrick",
			"receiver_contact":"0705622625",
			"size":"Small Parcel: Documents, Envelope items. less than 20KGs"}

parcel1 = Parcel(initDict1)
parcel2 = Parcel(initDict2)
parcel3 = Parcel(initDict3)
parcel4 = Parcel(initDict4)
parcel5 = Parcel(initDict5)
parcel6 = Parcel(initDict6)
parcel7 = Parcel(initDict7)

user1 = User(1, "Anorld Mukone", "manorldsapiens@gmail.com", "123456")
user2 = User(2, "Mukisa Ronald", "r_mukisa@gmail.com", "2018codechef")
user3 = User(3, "Wakaby Paul", "wp2011@yahoo.com", "thebestintheworld")

admin1 =Admin(4, "Shelton Godwin", "shelton@live.com", "le_admin", True)


my_parcels = [parcel1, parcel2, parcel3, parcel4, parcel5, parcel6, parcel7]
my_users = [user1, user2, user3]
my_admins = [admin1]