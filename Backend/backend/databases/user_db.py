from datetime import date

import encryption
from databases.db_handler import DBHandler as db_handler
from models import user
from returns import return_json


class User_db(db_handler):
    def __init__(self):
        super().__init__("users")

    def get_all_users(self):
        result = []
        # Get all users and ignore _Id (standard mongodb id)
        #  because object id's can't be parsed to json
        users = self.find_all()
        for l_user in users:
            c_user = user.User()
            c_user.from_mongo(l_user)
            result.append(c_user.json())
        if result is not None:
            return [True, result]
        return [False]

    def get_user(self, email=None, uuid=None):
        querry = None
        if email is not None:
            querry = {"email": str(email)}

        elif uuid is not None:
            querry = {"uuid": str(uuid)}

        if querry is None:
            return [False, "No filter set"]

        res = self.find_one(querry)

        if res is None:
            return [False, "User not found"]
        c_user = user.User()
        c_user.from_mongo(res)
        return [True, c_user]

    def update_user(self, c_user: user):
        self.update_one({"uuid": c_user.uuid},
                        {"$set": c_user.json()})

    def insert_user(self, name, user_hash, email, birthdate):
        result = self.find_one({"email": email})
        if result is not None:
            return [False]

        new_user = user.User(name, user_hash, email, birthdate)
        self.insert_one(new_user.json())
        return [True, new_user.uuid]

    def verify_user(self, email, password, install_id):
        res = self.get_user(email=email)

        if res[0] is not True:
            return return_json(success=False, error="User not found")

        c_user = res[1]

        if not c_user.is_verified:
            return return_json(success=False, error="Please confirm your account, an email has been sent to your inbox")

        user_hash = c_user.user_hash
        res = encryption.Encryption.verify_password(password, user_hash)

        if res is False:
            return return_json(success=False, error="Password does not match")

        c_user.last_login = date.today()

        c_user.install_id = install_id  # Update the unique ID of the app

        self.update_user(c_user)

        return return_json(success=True, data={"uuid": c_user.uuid})
