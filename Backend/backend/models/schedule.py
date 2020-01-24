from models.event import Event
from returns import return_json
import datetime


class Schedule(object):
    def __init__(self, user_uuid: str = None, schedule: list = None):
        self.user_uuid = user_uuid
        if schedule is not None:
            self._schedule = schedule
        else:
            self._schedule = []

    def add_event(self, start=None, end=None, title=None, content=None, location=None, remind_minutes_before=None):
        if start is None \
            or end is None \
                or title is None:
            return [False, "Date, start, end & title needed"]

        new_event = Event(start, end, title, content,
                          location, remind_minutes_before)
        self._schedule.append(new_event.json())
        return [True, "Schedule was updated!"]

    def get_events(self):
        events = []
        for x_event in self._schedule:
            c_event = Event()
            c_event.from_mongo(x_event)

            events.append(c_event.json())
        return events

    def check_for_upcoming_events(self):
        current_time = datetime.datetime.today()
        upcoming_events = []
        for idx, l_event in enumerate(self._schedule):
            c_event = Event()
            c_event.from_mongo(l_event)
            if c_event.remind_minutes_before is not None:
                start_time = datetime.datetime.strptime(
                    c_event.start, "%d/%m/%Y %H:%M:%S")
                remaining_seconds = (start_time - current_time).total_seconds()
                # Convert seconds to days
                remaining_minutes = divmod(remaining_seconds, 60)[0]

                if remaining_minutes <= c_event.remind_minutes_before and remaining_minutes > 0:
                    # So that the notifications won't be send twice
                    c_event.remind_minutes_before = None
                    self._schedule[idx] = c_event.json()
                    upcoming_events.append(c_event)

        return upcoming_events

    def update_event(self, _event_uuid=None, new_event: Event = None):
        if _event_uuid is None or new_event is None:
            return [False, "No uuid or new_event set"]

        for idx, l_event in enumerate(self._schedule):
            if 'event_uuid' in l_event:
                c_event = Event()
                c_event.from_mongo(l_event)
                if c_event.event_uuid == _event_uuid:
                    self._schedule[idx] = new_event.json()
                    return [True, "event found and updated"]
        return [False, "event not found and updated"]

    def delete_event(self, _event_uuid=None, delete_all: bool = False):
        if delete_all:
            self._schedule = []
            return return_json(success=True, data={'message': 'Deleted all events'})
        for idx, l_event in enumerate(self._schedule):
            if 'event_uuid' in l_event:
                c_event = Event()
                c_event.from_mongo(l_event)
                if c_event.event_uuid == _event_uuid:
                    del self._schedule[idx]
                    return return_json(success=True, data={"message": "Deleted one event"})
        return return_json(success=False, error="Event not found")

    def from_mongo(self, mongo_data):
        self.user_uuid = mongo_data["user_uuid"]
        self._schedule = mongo_data["schedule"]

    def json(self):
        return {
            'user_uuid': self.user_uuid,
            'schedule': self._schedule
        }
