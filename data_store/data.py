
from app.models import *

parcel1 = Parcel(1, "i5261", 1, "Delivered", "Ssebagala stage, Kisasi", "Namakwekwe, Mbale", "2 CMA books", "0757877585", "Kitebe John", "0772449361", "Small Parcel: Documents, Envelope items. less than 20KGs")
parcel2 = Parcel(2, "i5659", 2, "Initiated by Client", "Garden City, 1st gate down from Jinja road", "Garden City, 2nd Level, Shop 32", "Women Jewellery", "0757877585", "Zimulati Nagudi", "0782203860", "Small Parcel: Documents, Envelope items. less than 20KGs")
parcel3 = Parcel(3, "i2562", 1, "Active", "Ssebagala stage, Kisasi", "Shell gas station, Kamwokya", "Gas Cannister", "0757877585", "Amos Lwegela", "075256656", "Medium Parcel: less than 65KGs")
parcel4 = Parcel(4, "i2562", 3, "Initiated by Client", "Boulevard, Kampala road, shop D52", "Ssebagala stage, Kisasi", "New Nokia 8", "0775225525", "Anorld Mukone", "0757877585", "Small Parcel: Documents, Envelope items. less than 20KGs")
parcel5 = Parcel(5, "i2531", 2, "Delivered", "Garden City, 1st gate down from Jinja road", "Ssebagala stage, Kisasi", "Space Cookies", "077256555", "Anorld Mukone", "0757877585", "Small Parcel: Documents, Envelope items. less than 20KGs")
parcel6 = Parcel(6, "i5426", 1, "Active", "Ssebagala stage, Kisasi", "Banda stage, Jinja road", "Sauce pans", "0757877585", "Emma Richard", "0705256546", "Medium Parcel: less than 65KGs")
parcel7 = Parcel(7, "i5565", 1, "Initiated by Client", "Ssebagala stage, Kisasi", "Banda stage, Jinja road", "Need 4 speed cd", "0757877585", "Ian Kendrick", "0705622625", "Small Parcel: Documents, Envelope items. less than 20KGs")

user1 = User(1, "Anorld Mukone", "manorldsapiens@gmail.com", "123456")
user2 = User(2, "Mukisa Ronald", "r_mukisa@gmail.com", "2018codechef")
user3 = User(3, "Wakaby Paul", "wp2011@yahoo.com", "thebestintheworld")


my_parcels = [parcel1, parcel2, parcel3, parcel4, parcel5, parcel6, parcel7]
my_users = [user1, user2, user3]