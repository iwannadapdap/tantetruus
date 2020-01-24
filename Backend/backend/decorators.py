from functools import wraps

from flask import session, url_for

import app_config
from returns import return_json, return_message
from databases import admin_db
from sessions import TtSession

db = admin_db.Admin_db()

'''
def admin_panel_enabled(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if app_config.ADMIN_PANEL_ENABLED:
            return f(*args, **kwargs)

        return return_json(success=False, error="Admin panel disabled")

    return decorated_function
'''


def valid_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        adminSession = TtSession(session)

        if adminSession.admin_username is None \
                or adminSession.admin_password is None:
            return return_message("error", "You are not logged into an admin account", 2, url_for('admin_blueprint.login'))

        if adminSession.admin_username != app_config.ADMIN_EMAIL \
                or adminSession.admin_password != app_config.ADMIN_PASSWORD:
            return return_message("error", "You do not have acces to this account", 2, url_for('admin_blueprint.login'))
        return f(*args, **kwargs)
    return decorated_function
