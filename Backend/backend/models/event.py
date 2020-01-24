import uuid
from datetime import datetime


class Event(object):
    def __init__(self, start=None, end=None, title=None, content=None,
                 location=None, remind_minutes_before=None):
        self.event_uuid = str(uuid.uuid4())
        self.start = start
        self.end = end
        self.title = title
        self.content = content
        self.location = location
        self.remind_minutes_before = remind_minutes_before
        self.created_at = datetime.now()

    def from_mongo(self, mongo_data: dict):
        self.event_uuid = mongo_data['event_uuid']
        self.start = mongo_data['start']  # 15/06/2009 13:45
        self.end = mongo_data['end']  # 15/06/2009 13:45
        self.title = mongo_data['title']
        self.content = mongo_data['content']
        self.location = mongo_data['location']
        self.remind_minutes_before = mongo_data['remind_minutes_before']
        self.created_at = mongo_data['created_at']

    def json(self):
        return {
            'event_uuid': self.event_uuid,
            'start': self.start,
            'end': self.end,
            'title': self.title,
            'content': self.content,
            'location': self.location,
            'remind_minutes_before': self.remind_minutes_before,
            'created_at': self.created_at
        }
