from flask import Blueprint, jsonify, redirect, request, session, url_for

import datetime
from databases import user_db, arduino_db
from encryption import Encryption
from models import arduino
from returns import return_json
import data_validation


user_blueprint = Blueprint('user_blueprint', __name__)
user_prefix = "/user"

user_db = user_db.User_db()
arduino_db = arduino_db.Arduino_db()


@user_blueprint.route(user_prefix + "/get", methods=["POST"])
def get_user():
    user_uuid = request.form.get("uuid", None)
    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if user_db.get_user(uuid=user_uuid)[0] is False:
        return return_json(success=False, error="User not found")

    c_user = user_db.get_user(uuid=user_uuid)[1]
    result = {
        'uuid': c_user.uuid,
        'name': c_user.name,
        'email': c_user.email,
        'birthdate': c_user.birthdate,
        'last_login': c_user.last_login,
        'created_at': c_user.created_at
    }

    return return_json(success=True, data=result)


@user_blueprint.route(user_prefix + "/update", methods=["POST"])
def update_user():
    user_uuid = request.form.get("uuid", None)
    name = str(request.form.get("name", None))
    user_hash = Encryption.encrypt_password(
        str(request.form.get("password", None))
    )
    email = str(request.form.get("email", None))
    birthdate = str(request.form.get("birthdate", None))

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if user_db.get_user(uuid=user_uuid)[0] is False:
        return return_json(success=False, error="User not found")

    if not data_validation.validate_email(email):
        return return_json(success=False, error="Invalid email")

    if not data_validation.validate_birthdate(birthdate)[0]:
        return return_json(
            success=False, error=data_validation.validate_birthdate(birthdate)[1])

    c_user = user_db.get_user(uuid=user_uuid)[1]

    c_user.name = name
    c_user.user_hash = user_hash
    if c_user.email != email:
        c_user.email = email
        c_user.is_verified = False
    c_user.birthdate = birthdate

    user_db.update_user(c_user)

    return return_json(success=True, data={"message": "User {0} updated".format(c_user.uuid)})


@user_blueprint.route(user_prefix + "/preferences/update", methods=["POST"])
def toggle_notifications():
    user_uuid = request.form.get("uuid", None)
    r_notifications_enabled = request.form.get("notifications_enabled", None)
    r_alarm_enabled = request.form.get("alarm_enabled", None)

    if r_alarm_enabled is not None:
        if r_alarm_enabled.lower() == "true":
            r_alarm_enabled = True
        elif r_alarm_enabled.lower() == "false":
            r_alarm_enabled = False
        else:
            return return_json(success=False, error="Invalid alarm_enabled bool: true | false")
    else:
        return return_json(success=False, error="alarm_enabled must be set")

    if r_notifications_enabled is not None:
        if r_notifications_enabled.lower() == "true":
            r_notifications_enabled = True
        elif r_notifications_enabled.lower() == "false":
            r_notifications_enabled = False
        else:
            return return_json(success=False, error="Invalid notifications enabled bool: true | false")
    else:
        return return_json(success=False, error="notifications_enabled must be set")

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if user_db.get_user(uuid=user_uuid)[0] is False:
        return return_json(success=False, error="User not found")

    c_user = user_db.get_user(uuid=user_uuid)[1]

    c_user.notifications_enabled = r_notifications_enabled
    c_user.alarm_enabled = r_alarm_enabled

    user_db.update_user(c_user)
    return return_json(success=True, data={'notifications_enabled': c_user.notifications_enabled,
                                           'alarm_enabled': c_user.alarm_enabled})


@user_blueprint.route(user_prefix + "/preferences/get", methods=["POST"])
def get_preferences():
    user_uuid = request.form.get("uuid", None)
    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if user_db.get_user(uuid=user_uuid)[0] is False:
        return return_json(success=False, error="User not found")

    c_user = user_db.get_user(uuid=user_uuid)[1]

    return return_json(success=True, data={"preferences": {
        'notifications_enabled': c_user.notifications_enabled,
        'alarm_enabled': c_user.alarm_enabled
    }})


@user_blueprint.route(user_prefix + "/link_arduino", methods=["POST"])
def set_arduino_uuid():
    user_uuid = request.form.get("uuid", None)
    arduino_uuid = request.form.get("arduino_uuid", None)

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if not data_validation.validate_uuid(arduino_uuid):
        return return_json(success=False, error="Invalid arduino UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    if arduino_db.get_user_uuid_by_arduino_uuid(arduino_uuid):
        c_user_uuid = arduino_db.get_user_uuid_by_arduino_uuid(arduino_uuid)
        if c_user_uuid:  # If the user has an arduino linked we need to remove it from that arduino
            c_arduino_mongo = arduino_db.find_one(
                {'arduino_uuid': arduino_uuid})
            c_arduino = arduino.Arduino.from_mongo(c_arduino_mongo)
            c_arduino.user_uuid = None
            arduino_db.update_one({'arduino_uuid': arduino_uuid},
                                  {"$set": c_arduino.json()})

    return arduino_db.link_arduino(arduino_uuid, user_uuid)
