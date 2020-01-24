from encryption import Encryption
from app_config import ADMIN_EMAIL, ADMIN_PASSWORD
from databases.db_handler import DBHandler as db_handler
from models import admin, user
from returns import return_json


class Admin_db(db_handler):
    def __init__(self):
        super().__init__("admins")

    def verify_admin(self, email, password):
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            return True
        return False

    """
    def insert_admin(self, name, user_hash, email):

        result = self.find_one({"email": email})

        if result is not None:
            return [False, "Email already exists"]
        new_admin = admin.Admin(name, user_hash, email)
        self.insert_one(new_admin.json())
        return [True, new_admin.uuid]

    def get_admin(self, email=None, uuid=None):
        querry = None
        if email is not None:
            querry = {"email": str(email)}

        elif uuid is not None:
            querry = {"uuid": uuid}

        if querry is None:
            return [False, "No filter set"]

        res = self.find_one(querry)

        if res is None:
            return [False, "Admin not found!"]
        return [True, res]
    
    def verify_admin(self, email=None, password=None):
        res = self.get_admin(email=email)

        if res[0] is not True:
            return [False, 0, "Email not found"]

        c_admin = res[1]
        admin_hash = c_admin["user_hash"]
        res = Encryption.verify_password(password, admin_hash)

        if res:
            return [True, "Login successfull", admin]
        return [False, 1, "No match"]

    def validate_admin(self, uuid: str = None):
        if uuid is not None:
            if(self.find_one({'uuid': uuid})):
                return [True]
            return [False, "No admin found"]
        return [False, "No uuid set"]
    """
