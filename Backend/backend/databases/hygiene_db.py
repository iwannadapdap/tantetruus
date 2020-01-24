from databases.db_handler import DBHandler as db_handler
from models import hygiene
from returns import return_json


class Hygiene_db(db_handler):
    def __init__(self):
        super().__init__("hygienes")

    def create_hygiene(self, user_uuid: str):
        new_hygiene = hygiene.Hygiene(user_uuid)
        self.insert_one(new_hygiene.json())

    def get_user_hygiene(self, user_uuid: str):
        return self.find_one({'user_uuid': user_uuid})

    def update_reminders(self, user_uuid: str, notifications: dict):
        res = self.get_user_hygiene(user_uuid)
        c_hygienes = hygiene.Hygiene()
        c_hygienes.from_mongo(res)

        if c_hygienes.update_notifiations(notifications):
            if self.update_one({'user_uuid': user_uuid}, {"$set": c_hygienes.json()}):
                return return_json(success=True)
            return return_json(success=False, error="Database could not be updated")
        return return_json(success=False, error="Something went wrong")
