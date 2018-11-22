import uuid
from app.models.Admin import Admin
from app.models.User import User

admin_data = {"name":"Mr Admin", "email":"admin@sendit.com", "password":"sfa1a1AAdfa12"}
my_admin_original = Admin(admin_data)

admin_login = {"email":"admin@sendit.com", "password":"sfa1a1AAdfa12"}

my_admins = [my_admin_original]