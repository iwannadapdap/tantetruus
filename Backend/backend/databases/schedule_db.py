from databases.db_handler import DBHandler as db_handler
from models import user, event, schedule
from returns import return_json
from data_validation import validate_uuid
from datetime import datetime


class Schedule_db(db_handler):
    def __init__(self):
        super().__init__("schedules")

    def create_schedule(self, user_uuid: str):
        self.insert_one(schedule.Schedule(user_uuid).json())

    def get_user_schedule(self, user_uuid):
        res = self.find_one({'user_uuid': user_uuid})

        if not res:
            return return_json(success=False, error="No schedule found")

        c_schedule = schedule.Schedule()
        c_schedule.from_mongo(res)

        return c_schedule

    def get_user_schedule_by_date(self, user_uuid, date):
        res = self.find_one({'user_uuid': user_uuid})

        if not res:
            return return_json(success=False, error="No schedule found")

        c_schedule = schedule.Schedule()
        c_schedule.from_mongo(res)

        c_schedule = c_schedule.get_events()

        selected_date = datetime.strptime(date.split(" ", 1)[0], "%d/%m/%Y")
        r_schedule = []

        for l_event in c_schedule:
            c_event = event.Event()
            c_event.from_mongo(l_event)

            event_start = datetime.strptime(
                c_event.start.split(" ", 1)[0], "%d/%m/%Y")
            print(event_start == selected_date)
            if event_start == selected_date:
                r_schedule.append(c_event.json())
        return r_schedule

    def delete_event(self, user_uuid: str, event_uuid: str, delete_all: bool):
        res = self.find_one({'user_uuid': user_uuid})

        if not res:
            return return_json(success=False, error="No schedule found")

        c_schedule = schedule.Schedule()
        c_schedule.from_mongo(res)
        res = c_schedule.delete_event(event_uuid, delete_all)
        self.update_one({'user_uuid': user_uuid}, {"$set": c_schedule.json()})
        return res

    def update_schedule(self, user_uuid, start, end, title, content, location, remind_minutes_before, event_uuid=None):
        res = self.find_one({'user_uuid': user_uuid})

        if not res:
            return return_json(success=False, error="No schedule found")

        c_schedule = schedule.Schedule()
        c_schedule.from_mongo(res)

        if event_uuid is not None:
            # update reminder
            if not validate_uuid(event_uuid):
                return return_json(success=False, error="Invalid event UUID")

            res = c_schedule.update_event(event_uuid,
                                          event.Event(start, end, title, content, location, remind_minutes_before))
            if res[0] is False:
                return return_json(success=False, error="Reminder not found")

            self.update_one({'user_uuid': c_schedule.user_uuid},
                            {"$set": c_schedule.json()})

            return return_json(success=True)

        res = c_schedule.add_event(
            start, end, title, content, location, remind_minutes_before)

        if res is False:
            return return_json(success=False, error="Fields empty")

        self.update_one({'user_uuid': c_schedule.user_uuid},
                        {"$set": c_schedule.json()})
        return return_json(success=True)
