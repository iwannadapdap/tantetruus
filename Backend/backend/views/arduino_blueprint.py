from flask import Blueprint, request
from notifications import send_notification_to_user
from databases import schedule_db, user_db, arduino_db
from returns import return_json
from models.event import Event
import data_validation

arduino_blueprint = Blueprint('arduino_blueprint', __name__)
arduino_prefix = "/arduino"

user_db = user_db.User_db()
schedule_db = schedule_db.Schedule_db()
arduino_db = arduino_db.Arduino_db()


@arduino_blueprint.route(arduino_prefix + "/schedule/get", methods=["POST"])
def get_schedule():
    request_json = request.json

    if request_json["arduino_uuid"] is None:
        return return_json(succes=False, error="Arduino UUID is not set")

    arduino_uuid = request_json["arduino_uuid"]

    if not data_validation.validate_uuid(arduino_uuid):
        return return_json(success=False, error="Arduino UUID is not valid")

    # The maximum amount of events that can be returned due to limited memory
    try:
        max_events_amount = int(request_json["max_events_amount"])
    except TypeError:
        return return_json(success=False, error="Max_event_amounts must be a number")
    except KeyError:
        max_events_amount = 20

    if not data_validation.verify_arduino(arduino_uuid):
        return return_json(success=False, error="Arduino is not linked")

    c_user_uuid = arduino_db.get_user_uuid_by_arduino_uuid(arduino_uuid)

    res = user_db.get_user(uuid=c_user_uuid)

    if not res[0]:
        return return_json(success=False, error="User not found")

    c_user_uuid = res[1].uuid

    c_schedule = schedule_db.get_user_schedule(c_user_uuid).get_events()

    # User schedule
    if len(c_schedule) > max_events_amount:
        c_schedule = c_schedule[-max_events_amount:]

    for idx, l_item in enumerate(c_schedule):
        c_item = Event()
        c_item.from_mongo(l_item)
        c_schedule[idx] = {
            'start': c_item.start,
            'end': c_item.end,
            'title': c_item.title,
            'content': c_item.content,
            'location': c_item.location
        }

    return return_json(success=True, data={'schedule': c_schedule})


@arduino_blueprint.route(arduino_prefix + "/schedule/check_notifications", methods=["POST"])
def check_notifications():
    request_json = request.json

    if request_json["arduino_uuid"] is None:
        return return_json(succes=False, error="Arduino UUID is not set")

    arduino_uuid = request_json["arduino_uuid"]

    if not data_validation.validate_uuid(arduino_uuid):
        return return_json(success=False, error="Arduino UUID is not valid")

    if not data_validation.verify_arduino(arduino_uuid):
        return return_json(success=False, error="Arduino is not linked")

    try:
        max_events_amount = int(request_json["max_events_amount"])
    except TypeError:
        return return_json(success=False, error="Max_events_amount must be a number")
    except KeyError:
        max_events_amount = 20

    c_user_uuid = arduino_db.get_user_uuid_by_arduino_uuid(arduino_uuid)

    res = user_db.get_user(uuid=c_user_uuid)

    if not res[0]:
        return return_json(success=False, error="User not found")

    c_user = res[1]

    c_schedule = schedule_db.get_user_schedule(c_user.uuid)

    upcoming_events = c_schedule.check_for_upcoming_events()

    total_event_count = len(upcoming_events)

    return_events = []
    for c_event in upcoming_events:
        return_events.append(c_event.json())

    if len(return_events) > max_events_amount:
        return_events = return_events[-max_events_amount:]

    return return_json(success=True, data={'event_count': total_event_count, 'upcoming_events': return_events})


@arduino_blueprint.route(arduino_prefix + "/alarm/trigger", methods=["POST"])
def trigger_alarm():
    request_json = request.json

    if request_json["arduino_uuid"] is None:
        return return_json(succes=False, error="Arduino UUID is not set")

    arduino_uuid = request_json["arduino_uuid"]

    if not data_validation.validate_uuid(arduino_uuid):
        return return_json(success=False, error="Arduino UUID is not valid")

    if not data_validation.verify_arduino(arduino_uuid):
        return return_json(success=False, error="Arduino is not linked")

    c_user_uuid = arduino_db.get_user_uuid_by_arduino_uuid(arduino_uuid)

    res = user_db.get_user(uuid=c_user_uuid)

    if not res[0]:
        return return_json(success=False, error="User not found")

    c_user = res[1]

    if c_user.alarm_enabled:
        send_notification_to_user(
            c_user.install_id,
            "ALARM",
            "Motion detected near your TruusPod!"
        )
        return return_json(success=True, data={"message": "Notifications sent"})
    return return_json(success=False, error="Alarm is disabled")
