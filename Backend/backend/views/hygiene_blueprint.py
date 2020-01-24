from flask import Blueprint, request

from databases import hygiene_db
from returns import return_json
from models import hygiene
import data_validation

hygiene_blueprint = Blueprint('hygiene_blueprint', __name__)
hygiene_prefix = "/user/hygiene"

db = hygiene_db.Hygiene_db()


@hygiene_blueprint.route(hygiene_prefix + "/update", methods=["POST"])
def update_hygiene():
    user_uuid = str(request.form.get("uuid", None))
    hygiene_name_to_update = request.form.get("hygiene_name", None)
    hygiene_is_done = str(request.form.get("is_done", None))

    if hygiene_is_done is not None:
        if hygiene_is_done.lower() == "true":
            hygiene_is_done = True
        elif hygiene_is_done.lower() == "false":
            hygiene_is_done = False
        else:
            return return_json(success=False, error="Invalid delete all: true | false")
    else:
        hygiene_is_done = True

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    res = db.get_user_hygiene(user_uuid)

    c_hygienes = hygiene.Hygiene()
    c_hygienes.from_mongo(res)

    res = c_hygienes.update_hygiene(hygiene_name_to_update, hygiene_is_done)
    db.update_one({'user_uuid': user_uuid}, {"$set": c_hygienes.json()})
    return res


@hygiene_blueprint.route(hygiene_prefix + "/get", methods=["POST"])
def get_hygiene():
    user_uuid = str(request.form.get("uuid", None))

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    c_hygiene = db.get_user_hygiene(user_uuid)

    return return_json(success=True, data={"hygiene": c_hygiene})


@hygiene_blueprint.route(hygiene_prefix + "/update_reminders", methods=["POST"])
def update_reminders():
    user_uuid = str(request.form.get("uuid", None))

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    sheets_days = request.form.get("sheets", None)
    bathroom_days = request.form.get("bathroom", None)
    house_days = request.form.get("house", None)
    kitchen_days = request.form.get("kitchen", None)
    dishes_days = request.form.get("dishes", None)
    vacuum_days = request.form.get("vacuum", None)

    update_dict = {
        "sheets": sheets_days,
        "bathroom": bathroom_days,
        "house": house_days,
        "kitchen": kitchen_days,
        "dishes": dishes_days,
        "vacuum": vacuum_days
    }

    return db.update_reminders(user_uuid, update_dict)
