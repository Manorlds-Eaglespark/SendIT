import uuid
from app.models.Admin import Admin
from app.models.User import User

admin_data = {"id":int(uuid.uuid4().clock_seq), "name":"Mr Admin", "email":"admin@sendit.com", "password":"a1a1a12"}
my_admin_original = Admin(admin_data)

my_admins = [my_admin_original]