import uuid
from app.models.Admin import Admin
from app.models.User import User

admin_data = {"id":uuid.uuid4, "name":"Mr Admin", "email":"admin@sendit.com", "password":"a1a1a12"}
test_admin_functions = Admin(admin_data)

my_parcels = []
my_users = []
my_admins = [test_admin_functions]
my_quotations = []