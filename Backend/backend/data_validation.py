import re as regex
import unicodedata
from datetime import datetime
from databases.user_db import User_db as user_db
from databases.arduino_db import Arduino_db as arduino_db
from uuid import UUID


def verify_user(user_uuid: str):
    res = user_db().find_one({'uuid': user_uuid})
    if res is not None:
        return True
    return False


def verify_arduino(arduino_uuid: str):
    res = arduino_db().find_one({'arduino_uuid': arduino_uuid})

    if res is not None:
        return True
    return False


def validate_datetime(date_time: str):
    try:
        if date_time != datetime.strptime(date_time, "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S"):
            raise ValueError
        return [True, ""]
    except ValueError as e:
        return [False, str(e)]


def validate_start_before_end(start: str, end: str):
    start = datetime.strptime(
        start, "%d/%m/%Y %H:%M:%S")
    end = datetime.strptime(
        end, "%d/%m/%Y %H:%M:%S")

    if start > datetime.now():
        if start < end and start != end:
            return [True]
        return [False, "End has to be after start"]
    return [False, "Start can't be in the past"]


def validate_email(email: str):
    valid_mail_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

    if regex.search(valid_mail_regex, email):
        return True
    return False


def validate_birthdate(birthdate: str):
    try:
        if birthdate != datetime.strptime(birthdate, "%d/%m/%Y").strftime("%d/%m/%Y"):
            raise ValueError
        return [True, ""]
    except ValueError as e:
        return [False, str(e)]


def validate_uuid(uuid: str):
    try:
        parsed_uuid = UUID(uuid, version=4)
    except Exception:
        return False
    return uuid.replace("-", "") == parsed_uuid.hex


def validate_amount(amount):
    try:
        float(amount)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(amount)
        return True
    except (TypeError, ValueError):
        pass

    return False
