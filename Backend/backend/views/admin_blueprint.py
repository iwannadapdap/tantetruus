from flask import Blueprint, jsonify, redirect, request, session, url_for, render_template
import decorators
from databases import admin_db, user_db, arduino_db, food_db, expenses_db, schedule_db, hygiene_db
from encryption import Encryption
from models import event, schedule, user, recipe, arduino
from returns import return_json, return_message
from token_generator import generate_confirm_token
from notifications import send_notification_to_user
import mail
import sessions
import data_validation

admin_blueprint = Blueprint('admin_blueprint', __name__)
admin_prefix = "/admin"

db = admin_db.Admin_db()
user_db = user_db.User_db()
arduino_db = arduino_db.Arduino_db()
food_db = food_db.Food_db()
expenses_db = expenses_db.Expense_db()
schedule_db = schedule_db.Schedule_db()
hygiene_db = hygiene_db.Hygiene_db()


@admin_blueprint.route(admin_prefix + "/", methods=["GET"])
@decorators.valid_admin
def admin_home():
    return render_template("admin/admin_main.html")


#####################################
#####################################
##                                 ##
##            USER ROUTES          ##
##                                 ##
#####################################
#####################################

@admin_blueprint.route(admin_prefix + "/users", methods=["GET"])
@decorators.valid_admin
def users_main():
    return render_template('users/user_main.html')


@admin_blueprint.route(admin_prefix + "/users/add", methods=["GET", "POST"])
@decorators.valid_admin
def add_user():
    if request.method == "GET":
        return render_template('users/user_add.html')

    name = str(request.form.get("name", None))
    pw1 = request.form.get("password", None)
    pw2 = request.form.get("confirm_password", None)
    user_hash = Encryption.encrypt_password(
        str(request.form.get("password", None))
    )
    email = str(request.form.get("email", None))
    birthdate = str(request.form.get("birthdate", None)).replace(
        "-", "/")  # IOS uses '-' instead of '/'

    if name is None or email is None or name is None:
        return render_template('users/user_add.html', error="Fields empty")
    if pw1 != pw2:
        return render_template('users/user_add.html', error="Passwords don't match")

    if not data_validation.validate_email(email):
        return render_template('users/user_add.html', error="Invalid mail")

    if not data_validation.validate_birthdate(birthdate)[0]:
        return render_template('users/user_add.html', error="Invalid birthdate:" + data_validation.validate_birthdate(birthdate)[1])

    res = user_db.insert_user(name, user_hash, email, birthdate)
    if not res[0]:
        return render_template('users/user_add.html', error="User already exists")

    user_uuid = res[1]
    expenses_db.create_expenses(user_uuid)
    schedule_db.create_schedule(user_uuid)
    hygiene_db.create_hygiene(user_uuid)

    token = generate_confirm_token(email)

    mail.send_confirmation_mail(name, email, token)
    return return_message("Succes", "User added!", 2, url_for('admin_blueprint.get_users'))


@admin_blueprint.route(admin_prefix + "/users/get", methods=["GET"])
@decorators.valid_admin
def get_users():
    all_users = user_db.get_all_users()

    if all_users[0]:
        users_and_arduinos = list()

        for l_user in all_users[1]:
            c_user = user.User()
            c_user.from_mongo(l_user)
            c_arduino = arduino_db.get_arduino_by_user_uuid(c_user.uuid)
            users_and_arduinos.append({"user": c_user, "arduino": c_arduino})

        return render_template("/users/user_list.html", user_list=users_and_arduinos)
    else:
        return render_template("/users/user_list.html", users=None)


@admin_blueprint.route(admin_prefix + "/user/<uuid>", methods=["GET"])
@decorators.valid_admin
def user_detail(uuid):
    c_user = user_db.get_user(uuid=uuid)
    if not c_user[0]:
        return return_message("Error", "User not found", 2, url_for("admin_blueprint.get_users"))
    c_arduino = arduino_db.get_arduino_by_user_uuid(uuid)
    return render_template('/users/user_detail.html', user_list=[{'user': c_user[1], 'arduino': c_arduino}])


@admin_blueprint.route(admin_prefix + "/user/<uuid>/delete", methods=["GET"])
@decorators.valid_admin
def user_delete(uuid):
    successes = []
    successes.append(user_db.delete_one({'uuid': uuid}))
    successes.append(expenses_db.delete_one({'user_uuid': uuid}))
    successes.append(schedule_db.delete_one({'user_uuid': uuid}))
    successes.append(hygiene_db.delete_one({'user_uuid': uuid}))

    if all(successes):
        return return_message("Succes", "User deleted", 2, url_for('admin_blueprint.get_users'))


@admin_blueprint.route(admin_prefix + "/user/<uuid>/edit", methods=["GET", "POST"])
@decorators.valid_admin
def user_edit(uuid):
    c_user = user_db.get_user(uuid=uuid)[1]
    if request.method == "GET":
        c_arduino = arduino_db.get_arduino_by_user_uuid(uuid)
        if c_arduino:
            c_user.arduino = c_arduino.arduino_uuid
        else:
            c_user.arduino = None
        return render_template('users/user_edit.html', user_list=[c_user])
    else:
        user_uuid = uuid
        name = str(request.form.get("name", None))
        email = str(request.form.get("email", None))
        birthdate = str(request.form.get("birthdate", None))

        if not data_validation.validate_uuid(user_uuid):
            return render_template('users/user_edit.html', user_list=[c_user], error="Invalid user UUID")

        if user_db.get_user(uuid=user_uuid)[0] is False:
            return render_template('users/user_edit.html', user_list=[c_user], error="User not found")

        if not data_validation.validate_email(email):
            return render_template('users/user_edit.html', user_list=[c_user], error="Invalid email")

        if not data_validation.validate_birthdate(birthdate)[0]:
            return render_template('users/user_edit.html', user_list=[c_user], error=data_validation.validate_birthdate(birthdate)[1])

        c_user = user_db.get_user(uuid=user_uuid)[1]

        c_user.name = name
        if c_user.email != email:
            c_user.email = email
            c_user.is_verified = False
            name = c_user.name

            token = generate_confirm_token(c_user.email)

            send_mail(c_user.name, c_user.email, token)

        c_user.birthdate = birthdate

        user_db.update_user(c_user)

        return return_message("User updated", f"{c_user.name} has been updated!", 2, url_for('admin_blueprint.get_users'))

#####################################
#####################################
##                                 ##
##            FOOD ROUTES          ##
##                                 ##
#####################################
#####################################


@admin_blueprint.route(admin_prefix + "/recipes", methods=["GET"])
@decorators.valid_admin
def recipes_main():
    return render_template("/recipes/recipe_main.html")


@admin_blueprint.route(admin_prefix + "/recipes/get", methods=["GET"])
@decorators.valid_admin
def get_recipes():
    all_recipes = food_db.get_recipes()

    return render_template("/recipes/recipe_list.html", recipe_list=all_recipes)


@admin_blueprint.route(admin_prefix + "/recipes/add", methods=["GET", "POST"])
@decorators.valid_admin
def add_recipe():
    if request.method == "GET":
        return render_template('recipes/recipe_add.html')

    title = request.form.get("title", None)
    prep_time = request.form.get("prep_time", None)
    ingredients = str(request.form.get("ingredients", None)).splitlines()
    preperation = str(request.form.get("preperation", None)).splitlines()

    ingredients = [x for x in ingredients if x.strip(' ')]
    preperation = [x for x in preperation if x.strip(' ')]

    food_db.add_recipe(title, prep_time, ingredients, preperation)

    return return_message("Succes", "Recipe Added", 2, url_for('admin_blueprint.get_recipes'))


@admin_blueprint.route(admin_prefix + "/recipe/<uuid>", methods=["GET"])
@decorators.valid_admin
def recipe_detail(uuid):
    c_recipe = food_db.get_recipe(uuid)
    if not c_recipe:
        return return_message("Error", "Recipe not found", 2, url_for("admin_blueprint.get_recipes"))

    return render_template('/recipes/recipe_detail.html', recipe_list=[c_recipe])


@admin_blueprint.route(admin_prefix + "/recipe/<uuid>/delete", methods=["GET"])
@decorators.valid_admin
def recipe_delete(uuid):
    if food_db.delete_one({'recipe_uuid': uuid}):
        return return_message("Succes", "Recipe deleted", 2, url_for('admin_blueprint.get_recipes'))


@admin_blueprint.route(admin_prefix + "/recipe/<uuid>/edit", methods=["GET", "POST"])
@decorators.valid_admin
def recipe_edit(uuid):
    c_recipe = food_db.get_recipe(uuid)
    if not c_recipe:
        return return_message("Error", "Recipe not found", 2, url_for("admin_blueprint.get_recipes"))

    if request.method == "GET":
        return render_template('/recipes/recipe_edit.html', recipe_list=[c_recipe])

    title = request.form.get("title", None)
    prep_time = request.form.get("prep_time", None)
    ingredients = str(request.form.get("ingredients", None)).splitlines()
    preperation = str(request.form.get("preperation", None)).splitlines()

    c_recipe.title = title
    c_recipe.prep_time = prep_time
    c_recipe.ingredients = [x for x in ingredients if x.strip(' ')]
    c_recipe.preperation = [x for x in preperation if x.strip(' ')]
    success = food_db.update_one({'recipe_uuid': c_recipe.recipe_uuid}, {
        "$set": c_recipe.json()})
    if success:
        return return_message("Succes", "Recipe editted", 2, url_for('admin_blueprint.get_recipes'))


#####################################
#####################################
##                                 ##
##            ARDUINO ROUTES       ##
##                                 ##
#####################################
#####################################

@admin_blueprint.route(admin_prefix + "/arduinos", methods=["GET"])
@decorators.valid_admin
def arduinos_main():
    return render_template('arduinos/arduinos_main.html')


@admin_blueprint.route(admin_prefix + "/arduinos/add", methods=["GET", "POST"])
@decorators.valid_admin
def arduinos_add():
    if request.method == "GET":
        return render_template('arduinos/arduinos_add.html')

    arduino_uuid = str(request.form.get('arduino_uuid', None)).strip()
    user_uuid = str(request.form.get('user_uuid', None)).strip()
    # If arduino_uuid is set, check if it's valid. If it's not return an error
    if arduino_uuid != "" and not data_validation.validate_uuid(arduino_uuid):
        return render_template('arduinos/arduinos_add.html', error="Invalid arduino UUID")
    if user_uuid != "" and not data_validation.validate_uuid(user_uuid):
        return render_template('arduinos/arduinos_add.html', error="Invalid user UUID")

    if arduino_uuid:
        new_arduino = arduino.Arduino(arduino_uuid=arduino_uuid)
        if user_uuid:
            new_arduino.user_uuid = user_uuid
            arduino_db.insert_one(new_arduino.json())
            return return_message("Succes", f"Arduino created with {arduino_uuid} and linked with {user_uuid}", 2, url_for('admin_blueprint.arduinos_get'))

        arduino_db.insert_one(new_arduino.json())
        return return_message("Succes", f"Arduino created with {arduino_uuid}", 2, url_for('admin_blueprint.arduinos_get'))
    else:
        arduino_db.create_arduino()
        return return_message("Succes", "Arduino created", 2, url_for('admin_blueprint.arduinos_get'))


@admin_blueprint.route(admin_prefix + "/arduinos/get", methods=["GET"])
@decorators.valid_admin
def arduinos_get():
    all_arduinos = arduino_db.get_all_arduinos()
    return render_template('arduinos/arduinos_list.html', arduino_list=all_arduinos)


@admin_blueprint.route(admin_prefix + "/arduinos/<uuid>", methods=["GET"])
@decorators.valid_admin
def arduino_detail(uuid):
    c_arduino = arduino_db.get_arduino(uuid)
    if not c_arduino:
        return return_message("Error", "Arduino not found", 2, url_for("admin_blueprint.arduinos_get"))

    return render_template('/arduinos/arduinos_detail.html', arduino_list=[c_arduino])


@admin_blueprint.route(admin_prefix + "/arduinos/<uuid>/delete", methods=["GET"])
@decorators.valid_admin
def arduino_delete(uuid):
    if arduino_db.delete_one({'arduino_uuid': uuid}):
        return return_message("Succes", "Arduino deleted", 2, url_for('admin_blueprint.arduinos_get'))


@admin_blueprint.route(admin_prefix + "/arduinos/<uuid>/edit", methods=["GET", "POST"])
@decorators.valid_admin
def arduino_edit(uuid):
    c_arduino = arduino_db.get_arduino(uuid)
    if not c_arduino:
        return return_message("Error", "Arduino not found", 2, url_for("admin_blueprint.arduinos_get"))

    if request.method == "GET":
        return render_template('arduinos/arduinos_edit.html', arduino_list=[c_arduino], user_list=user_db.get_all_users()[1])

    user_uuid = str(request.form.get('selected_user', None)).strip()
    print(user_uuid)
    # If arduino_uuid is set, check if it's valid. If it's not return an error
    if user_uuid != "" and not data_validation.validate_uuid(user_uuid):
        return render_template('arduinos/arduinos_edit.html', arduino_list=[c_arduino], user_list=user_db.get_all_users()[1], error="Invalid user UUID")

    c_arduino.user_uuid = user_uuid
    arduino_db.update_arduino(c_arduino)
    return return_message("Succes", "Arduino editted", 2, url_for("admin_blueprint.arduinos_get"))

#####################################
#####################################
##                                 ##
##            EMAIL ROUTES         ##
##                                 ##
#####################################
#####################################


@admin_blueprint.route(admin_prefix + "/email", methods=["GET"])
@decorators.valid_admin
def email_main():
    return render_template("email/email_main.html")


@admin_blueprint.route(admin_prefix + "/email/<uuid>", methods=["GET"])
@decorators.valid_admin
def email_main_uuid(uuid):
    c_user = user_db.get_user(uuid=uuid)
    return render_template("email/email_main.html", user=c_user[1])


@admin_blueprint.route(admin_prefix + "/email/send", methods=["POST"])
@decorators.valid_admin
def send_email_admin():
    email = request.form.get("email", None)
    subject = request.form.get("subject", None)
    content = request.form.get("content", None)

    if not data_validation.validate_email(email):
        return render_template('email/email_main.html', error="Invalid email")

    res = user_db.get_user(email=email)

    if not res[0]:
        return return_message("Error", "User not found", 2, url_for('admin_blueprint.email_main'))

    c_user = res[1]

    mail.send_message_mail(c_user.name, c_user.email, subject, content)

    return return_message("Succes", f"Email has been sent to {c_user.name}", 2, url_for("admin_blueprint.users_main"))


@admin_blueprint.route(admin_prefix + "/email/resend_verification_email/<uuid>")
@decorators.valid_admin
def resend_verification_email(uuid):
    res = user_db.get_user(uuid=uuid)

    if not res[0]:
        return return_message("Error", "User not found", 2, url_for("admin_blueprint.get_users"))

    c_user = res[1]

    if c_user.is_verified:
        return return_message("Task failed successfully", "User was already verified", 2, url_for("admin_blueprint.get_users"))

    name = c_user.name

    token = generate_confirm_token(c_user.email)

    mail.send_confirmation_mail(name, c_user.email, token)

    return return_message("Succes", f"Email has been sent to {c_user.name}", 2, url_for("admin_blueprint.get_users"))


#####################################
#####################################
##                                 ##
##       NOTIFICATIONS ROUTES      ##
##                                 ##
#####################################
#####################################

@admin_blueprint.route(admin_prefix + "/notifications", methods=["GET"])
@decorators.valid_admin
def notifications_main():
    return render_template("notifications/notifications_main.html")


@admin_blueprint.route(admin_prefix + "/notifications/<uuid>", methods=["GET"])
@decorators.valid_admin
def notifications_main_uuid(uuid):
    c_user = user_db.get_user(uuid=uuid)
    return render_template("notifications/notifications_main.html", user=c_user[1])


@admin_blueprint.route(admin_prefix + "/notifications/send", methods=["POST"])
@decorators.valid_admin
def send_notification_admin():
    uuid = request.form.get("uuid", None)
    title = str(request.form.get("title", None))
    message = str(request.form.get("message", None))

    if not data_validation.validate_uuid(uuid):
        return render_template('notifications/notifications_main.html', error="Invalid UUID")

    res = user_db.get_user(uuid=uuid)

    if not res[0]:
        return return_message("Error", "User not found", 2, url_for('admin_blueprint.notifications_main'))

    c_user = res[1]

    if c_user.install_id:
        if c_user.notifications_enabled:
            send_notification_to_user(c_user.install_id, title, message)
            if res[0]:
                return return_message("Succes", f"Notifcation has been sent to {c_user.name}", 2, url_for("admin_blueprint.users_main"))
            return return_message("Error", res[1], 5, url_for('admin_blueprint.notifications_main'))
        return return_message("Error", "User has notifications disabled", 2, url_for("admin_blueprint.users_main"))
    return return_message("Error", "User has no FCM key", 2, url_for('admin_blueprint.users_main'))

#####################################
#####################################
##                                 ##
##            OTHER ROUTES         ##
##                                 ##
#####################################
#####################################


#####################################
#####################################
##                                 ##
##         DATABASE ROUTES         ##
##                                 ##
#####################################
#####################################

@admin_blueprint.route(admin_prefix + "/databases", methods=["GET"])
@decorators.valid_admin
def databases_main():
    return render_template('databases/databases_main.html')


@admin_blueprint.route(admin_prefix + "/databases/yeet_database", methods=["GET"])
@decorators.valid_admin
def dropDb():
    db.drop_all()
    return return_message("Succes", "Databases dropped", 2, url_for('admin_blueprint.admin_home'))


@admin_blueprint.route(admin_prefix + "/databases/delete_all_recipes", methods=["GET"])
@decorators.valid_admin
def recipe_delete_all():
    if food_db.drop_coll():
        return return_message("Succes", "All recipes deleted", 2, url_for('admin_blueprint.databases_main'))


@admin_blueprint.route(admin_prefix + "/databases/delete_all_users", methods=["GET"])
@decorators.valid_admin
def user_delete_all():
    successes = []
    successes.append(user_db.drop_coll())
    successes.append(expenses_db.drop_coll())
    successes.append(schedule_db.drop_coll())
    successes.append(hygiene_db.drop_coll())
    successes.append(arduino_db.unlink_all_arduinos())
    if all(successes):
        return return_message("Succes", "All users deleted", 2, url_for('admin_blueprint.databases_main'))
    return return_json(success=False, error=f"Success missing")


@admin_blueprint.route(admin_prefix + "/databases/delete_all_arduinos", methods=["GET"])
@decorators.valid_admin
def arduinos_delete_all():
    if arduino_db.drop_coll():
        return return_message("Succes", "All arduinos deleted", 2, url_for('admin_blueprint.databases_main'))

#####################################
#####################################
##                                 ##
##            AUTH ROUTES          ##
##                                 ##
#####################################
#####################################


@admin_blueprint.route(admin_prefix + "/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('auth/login.html')

    email = str(request.form.get("emailInput", None))
    password = str(request.form.get("passwordInput", None))

    if email is None or password is None:
        return return_json(success=False, error="Fields empty")

    if not data_validation.validate_email(email):
        return return_json(success=False, error="Invalid email")

    if not db.verify_admin(email, password):
        return return_json(success=False, error="Invalid credentials")

    admin_session = sessions.TtSession(session)
    admin_session.login_admin(email, password)
    admin_session.update_ses(session)

    return return_message("Loggin successfull", "Welcome Senpaii uWu <3 <3", 2, url_for('admin_blueprint.admin_home'))


@admin_blueprint.route(admin_prefix + "/logout", methods=["GET"])
@decorators.valid_admin
def logout():
    admin_session = sessions.TtSession(session)
    admin_session.logout_admin()
    admin_session.update_ses(session)
    return return_message("You are logged out!", "Good bye senpaiiii :(((", 2, url_for('admin_blueprint.login'))


'''
@admin_blueprint.route(admin_prefix + "/register", methods=["GET", "POST"])
def register_user():
    name = str(request.form.get("name", None))
    user_hash = Encryption.encrypt_password(
        str(request.form.get("password", None))
    )
    email = request.form.get("email", None)

    if name is None or email is None:
        return return_json(success=False, error="Fields empty")

    if not data_validation.validate_email(email):
        return return_json(success=False, error="Invalid email")

    res = db.insert_admin(name, user_hash, email)

    if res[0] is False:
        return return_json(success=False, error="Email exists")
    else:
        return return_json(success=True, data={'uuid': res[1]})  # admin uuid

    @admin_blueprint.route(admin_prefix + "/get_admins", methods=["POST"])
    @decorators.valid_admin
    def get_admins():
    res = db.get_all_admins().get_json()
    if res['success']:
        return return_json(success=True, data={'users': res['data']})
    return return_json(success=False, error=res['error'])

'''
