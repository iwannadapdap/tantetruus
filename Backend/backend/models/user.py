import datetime
import uuid

from models import hygiene


class User(object):
    def __init__(self, name=None, user_hash=None, email=None, birthdate=None):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.user_hash = user_hash
        self.email = email
        self.birthdate = birthdate
        self.install_id = None
        self.notifications_enabled = True
        self.alarm_enabled = True
        self.is_verified = False
        self.verified_on = None
        self.created_at = datetime.datetime.now()
        self.last_login = datetime.datetime.now()

    def from_mongo(self, mongo_input: dict):
        self.uuid = mongo_input['uuid']
        self.name = mongo_input['name']
        self.user_hash = mongo_input['user_hash']
        self.email = mongo_input['email']
        self.birthdate = mongo_input['birthdate']
        self.install_id = mongo_input['install_id']
        self.notifications_enabled = mongo_input['notifications_enabled']
        self.alarm_enabled = mongo_input['alarm_enabled']
        self.is_verified = mongo_input['is_verified']
        self.verified_on = mongo_input['verified_on']
        self.created_at = mongo_input['created_at']
        self.last_login = mongo_input['last_login']

    def json(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'user_hash': self.user_hash,
            'email': self.email,
            'birthdate': self.birthdate,
            'install_id': self.install_id,
            'notifications_enabled': self.notifications_enabled,
            'alarm_enabled': self.alarm_enabled,
            'is_verified': self.is_verified,
            'verified_on': self.verified_on,
            'created_at': str(self.created_at),
            'last_login': str(self.last_login)
        }
