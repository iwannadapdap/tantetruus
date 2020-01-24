import firebase_admin
import app_config
from returns import return_json
from databases import user_db, expenses_db, schedule_db, hygiene_db
from models import user, event, hygiene
from notification_templates import notificationMaker, NotifcationType
import datetime
import json

from firebase_admin import exceptions
from firebase_admin import messaging


user_db = user_db.User_db()
expenses_db = expenses_db.Expense_db()
schedule_db = schedule_db.Schedule_db()
hygiene_db = hygiene_db.Hygiene_db()

maker = notificationMaker()
api_key = app_config.FIREBASE_API_KEY
creds = firebase_admin.credentials.Certificate("./firebase_creds.json")

firebase = firebase_admin.initialize_app(
    credential=creds, options=None, name="Main")


def send_notification_to_user(user_install_id, title: str, message: str):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message
        ),
        token=user_install_id
    )
    try:
        res = messaging.send(message=message, app=firebase)
        print(res)
        return [True]
    except exceptions.InvalidArgumentError as e:
        print("Notification not send")
        return [False, str(e)]


def check_for_notifications():
    print("Checking for notifications")
    res = user_db.get_all_users()

    if res[0]:
        users = res[1]
    else:
        return return_json(success=False, error="No users in database")

    for l_user in users:
        c_user = user.User()
        c_user.from_mongo(l_user)
        if not c_user.install_id or not c_user.notifications_enabled:
            continue

        c_schedule = schedule_db.get_user_schedule(c_user.uuid)
        upcoming_events = c_schedule.check_for_upcoming_events()
        schedule_db.update_one({'user_uuid': c_user.uuid}, {
                               "$set": c_schedule.json()})

        res = hygiene_db.get_user_hygiene(c_user.uuid)
        c_hygiene = hygiene.Hygiene()
        c_hygiene.from_mongo(res)
        not_done_jobs = c_hygiene.check_hygiene()

        user_db.update_user(c_user)

        if upcoming_events:
            for c_event in upcoming_events:
                send_notification_to_user(
                    c_user.install_id,
                    c_event.title,
                    "Details: {0}\n Location: {1}".format(
                        c_event.content, c_event.location))

        for job in not_done_jobs:
            title, message = maker.get_notification_message(
                "hygiene", job.name)
            send_notification_to_user(
                c_user.install_id,
                title,
                message)
