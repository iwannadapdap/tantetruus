from datetime import date, datetime

from flask import Blueprint, request, render_template

from databases import user_db, expenses_db, schedule_db, hygiene_db
from encryption import Encryption
from returns import return_json
import token_generator
from mail import send_confirmation_mail
import data_validation

auth_blueprint = Blueprint("auth_blueprint", __name__)
auth_prefix = "/auth"

user_db = user_db.User_db()
expenses_db = expenses_db.Expense_db()
schedule_db = schedule_db.Schedule_db()
hygiene_db = hygiene_db.Hygiene_db()


@auth_blueprint.route(auth_prefix + "/register", methods=["POST"])
def register_user():
    name = str(request.form.get("name", None))
    user_hash = Encryption.encrypt_password(
        str(request.form.get("password", None))
    )
    email = str(request.form.get("email", None))
    birthdate = str(request.form.get("birthdate", None)).replace(
        "-", "/")  # IOS uses '-' instead of '/'

    if name is None or email is None or name is None:
        return return_json(success=False,
                           error="Fields empty")

    if not data_validation.validate_email(email):
        return return_json(success=False,
                           error="Invalid email")

    if not data_validation.validate_birthdate(birthdate)[0]:
        return return_json(success=False,
                           error="Invalid birthdate:" + data_validation.validate_birthdate(birthdate)[1])

    res = user_db.insert_user(name, user_hash, email, birthdate)
    if not res[0]:
        return return_json(success=False, error="User already exists")
    user_uuid = res[1]
    expenses_db.create_expenses(user_uuid)
    schedule_db.create_schedule(user_uuid)
    hygiene_db.create_hygiene(user_uuid)

    token = token_generator.generate_confirm_token(email)

    send_confirmation_mail(name, email, token)

    return return_json(success=True)


@auth_blueprint.route(auth_prefix + "/login", methods=["POST"])
def login():
    email = str(request.form.get("email", None))
    password = str(request.form.get("password", None))
    install_id = str(request.form.get("install_id", None))  # Unique app id
    if email is None or password is None:
        return return_json(success=False, error="Fields empty")

    if not data_validation.validate_email(email):
        return return_json(success=False, error="Invalid email")

    if install_id is None:
        return return_json(success=False, error="Invalid install_id")

    return user_db.verify_user(email, password, install_id)


@auth_blueprint.route(auth_prefix + '/confirm/<token>')
def confirm_email(token):
    try:
        email = token_generator.confirm_token(token)
    except Exception as e:
        return return_json(success=False, error="link has expired or is invalid, "+str(e))
    res = user_db.get_user(email=email)
    if res[0] is False:
        return return_json(success=False, error="User not found")

    c_user = res[1]
    if c_user.is_verified:
        return render_template('auth/confirmation_succes.html', name=c_user.name)

    c_user.is_verified = True
    c_user.verified_on = datetime.now()
    user_db.update_user(c_user)
    return render_template('auth/confirmation_succes.html', name=c_user.name)


@auth_blueprint.route(auth_prefix + '/resend_verification_email', methods=["POST"])
def resend_mail():
    email = request.form.get("email", None)

    if not data_validation.validate_email(email):
        return return_json(success=False, error="Invalid email")

    res = user_db.get_user(email=email)

    if not res[0]:
        return return_json(success=False, error="User not found")

    c_user = res[1]

    if c_user.is_verified:
        return return_json(success=False, error="User is already verified")

    name = c_user.name

    token = token_generator.generate_confirm_token(email)

    send_mail(name, email, token)

    return return_json(success=True)


@auth_blueprint.route(auth_prefix + "/register_fcm_key", methods=["POST"])
def check_key():
    c_fcm_key = request.form.get("fcm_key", None)
    user_uuid = request.form.get("uuid", None)

    if c_fcm_key is None:
        return return_json(success=False, error="No fcm_key set")

    if user_uuid is None:
        return return_json(success=False, error="No uuid set'")

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid uuid format")

    res = user_db.get_user(uuid=user_uuid)

    if not res[0]:
        return return_json(success=False, error="User not found")

    c_user = res[1]

    if c_user.install_id == c_fcm_key:
        return return_json(success=True)
    c_user.install_id = c_fcm_key
    user_db.update_user(c_user)

    return return_json(success=True)
