import datetime
import uuid


class Admin(object):
    def __init__(self, name=None, user_hash=None, email=None):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.user_hash = user_hash
        self.email = email
        self.created_at = datetime.datetime.now()

    def from_mongo(self, mongo_input: dict):
        self.uuid = mongo_input['uuid']
        self.name = mongo_input['name']
        self.user_hash = mongo_input['user_hash']
        self.email = mongo_input['email']
        self.created_at = mongo_input['created_at']

    def json(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'user_hash': self.user_hash,
            'email': self.email,
            'created_at': self.created_at
        }
