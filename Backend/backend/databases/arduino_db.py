from databases.db_handler import DBHandler
from models.arduino import Arduino
from returns import return_json
from uuid import uuid4


class Arduino_db(DBHandler):
    def __init__(self):
        super().__init__("arduinos")

    def create_arduino(self):
        new_arduino = Arduino(str(uuid4()))
        self.insert_one(new_arduino.json())

    def get_arduino(self, arduino_uuid: str):
        c_arduino = self.find_one({'arduino_uuid': arduino_uuid})
        if c_arduino:
            return Arduino.from_mongo(c_arduino)
        return None

    def link_arduino(self, arduino_uuid: str, user_uuid: str):
        res = self.find_one({'arduino_uuid': arduino_uuid})
        if res:
            c_arduino = Arduino.from_mongo(res)

            c_arduino.user_uuid = user_uuid
            self.update_arduino(c_arduino)
            return return_json(success=True, data={'message': 'Arduino linked successfully'})
        else:
            new_arduino = Arduino(arduino_uuid, user_uuid)
            res = self.insert_one(new_arduino.json())
            return return_json(success=True,
                               data={'message': 'New arduino created and linked successfully'})

    def unlink_all_arduinos(self):
        res = self.find_all()

        if res:
            for arduino in res:
                c_arduino = Arduino.from_mongo(arduino)

                c_arduino.user_uuid = None
                self.update_arduino(c_arduino)
        return True

    def get_user_uuid_by_arduino_uuid(self, arduino_uuid: str):
        res = self.find_one({'arduino_uuid': arduino_uuid})

        if not res:
            return False

        c_user_uuid = Arduino.from_mongo(res).user_uuid

        return c_user_uuid

    def get_arduino_by_user_uuid(self, user_uuid: str):
        res = self.find_one({'user_uuid': user_uuid})

        if res:
            c_arduino = Arduino.from_mongo(res)
            return c_arduino
        else:
            return None

    def update_arduino(self, c_arduino: Arduino):
        self.update_one({'arduino_uuid': c_arduino.arduino_uuid},
                        {'$set': c_arduino.json()})

    def get_all_arduinos(self):
        all_arduinos = self.find_all()

        r_arduinos = []
        for l_arduino in all_arduinos:
            c_arduino = Arduino.from_mongo(l_arduino)
            r_arduinos.append(c_arduino)

        return r_arduinos
