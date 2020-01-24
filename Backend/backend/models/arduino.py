from datetime import datetime


class Arduino():
    def __init__(self, arduino_uuid: str = None, user_uuid: str = None):
        self.user_uuid = user_uuid
        self.arduino_uuid = arduino_uuid
        self.created_at = datetime.now()

    @classmethod
    def from_mongo(cls, mongo_data: dict):
        return cls(mongo_data['arduino_uuid'], mongo_data['user_uuid'])

    def json(self):
        return {
            'user_uuid': self.user_uuid,
            'arduino_uuid': self.arduino_uuid
        }
