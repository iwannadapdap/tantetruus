from flask import Blueprint, request

from databases import schedule_db
from returns import return_json
import data_validation

schedule_blueprint = Blueprint('schedule_blueprint', __name__)
schedule_prefix = "/user/schedule"

db = schedule_db.Schedule_db()


@schedule_blueprint.route(schedule_prefix + "/get", methods=["POST"])
def get_schedule():
    user_uuid = str(request.form.get("uuid", None))

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    res = db.get_user_schedule(user_uuid).get_events()

    return return_json(success=True, data={'schedule': res})


@schedule_blueprint.route(schedule_prefix + "/get_date", methods=["POST"])
def get_schedule_by_date():
    user_uuid = str(request.form.get("uuid", None))
    date = str(request.form.get("date", None)).replace("-", "/")

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    if not data_validation.validate_birthdate(date):
        return return_json(success=False, error="Invalid date format: dd/mm/yyyy")

    res = db.get_user_schedule_by_date(user_uuid, date)

    return return_json(success=True, data={'schedule': res})


@schedule_blueprint.route(schedule_prefix + "/update", methods=["POST"])
def update_event():
    user_uuid = str(request.form.get("uuid", None))
    start = str(request.form.get("start", None)).replace(
        "-", "/")  # Ios datetime uses '-' instead of '/'
    end = str(request.form.get("end", None)).replace("-", "/")
    title = str(request.form.get("title", None))
    content = str(request.form.get("content", None))
    location = str(request.form.get("location", None))
    remind_minutes_before = request.form.get("remind_minutes_before", None)
    event_uuid = request.form.get("event_uuid", None)

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    if not data_validation.validate_datetime(start)[0]:
        return return_json(success=False, error=data_validation.validate_datetime(start)[1])

    if not data_validation.validate_datetime(end)[0]:
        return return_json(success=False, error=data_validation.validate_datetime(end)[1])

    time_validation = data_validation.validate_start_before_end(start, end)
    if not time_validation[0]:
        return return_json(success=False, error=time_validation[1])

    if remind_minutes_before is None:
        remind_minutes_before = 30  # Default value
    else:
        if not data_validation.validate_amount(remind_minutes_before):
            return return_json(success=False, error="remind_minutes_before must be a number")
        remind_minutes_before = int(remind_minutes_before)

    return db.update_schedule(user_uuid, start, end, title, content, location, remind_minutes_before, event_uuid)


@schedule_blueprint.route(schedule_prefix + "/delete", methods=["POST"])
def delete_event():
    user_uuid = str(request.form.get("uuid", None))
    event_uuid = request.form.get("event_uuid", None)
    delete_all = request.form.get("delete_all", None)
    if delete_all is not None:
        if delete_all.lower() == "true":
            delete_all = True
        elif delete_all.lower() == "false":
            delete_all = False
        else:
            return return_json(success=False, error="Invalid delete all: true | false")
    else:
        delete_all = False

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    return db.delete_event(user_uuid, event_uuid, delete_all)
