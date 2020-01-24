from flask import Flask, redirect, make_response
import app_config
import notifications
from databases.user_db import User_db
from views.admin_blueprint import admin_blueprint
from views.arduino_blueprint import arduino_blueprint
from views.auth_blueprint import auth_blueprint
from views.expenses_blueprint import expenses_blueprint
from views.schedule_blueprint import schedule_blueprint
from views.user_blueprint import user_blueprint
from views.hygiene_blueprint import hygiene_blueprint
from views.food_blueprint import food_blueprint

app = Flask(__name__)
app.secret_key = app_config.SECRET_KEY
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(expenses_blueprint)
app.register_blueprint(schedule_blueprint)
app.register_blueprint(arduino_blueprint)
app.register_blueprint(hygiene_blueprint)
app.register_blueprint(food_blueprint)


@app.route("/check_notifications", methods=["GET"])
def test_notifications():
    res = notifications.check_for_notifications()
    return str(res)


@app.route("/", methods=["GET"])
def home():
    return redirect('/admin')


@app.errorhandler(500)
def server_error_page(error):
    return redirect('https://youtu.be/qTksCYUgI7s')


@app.errorhandler(404)
def error_page(error):
    return redirect('https://www.youtube.com/watch?v=4qgrN6-JsOU')


user_db = User_db()


@app.context_processor
def get_user_list():
    return dict(user_list=user_db.get_all_users()[1])


if __name__ == "__main__":
    app.run(
        host=app_config.HOST,
        port=app_config.PORT,
        ssl_context=app_config.SSL_CONTEXT,
        debug=app_config.DEBUG,
    )
