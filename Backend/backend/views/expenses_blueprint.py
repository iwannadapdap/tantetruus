from flask import Blueprint, request

from databases import expenses_db
from returns import return_json
import data_validation

expenses_blueprint = Blueprint('expenses_blueprint', __name__)
expenses_prefix = "/user/expenses"

db = expenses_db.Expense_db()


@expenses_blueprint.route(expenses_prefix + "/update", methods=["POST"])
def update_expenses():
    user_uuid = str(request.form.get("uuid", None))
    expense_type = str(request.form.get("expense_type", None)).lower()
    est_amount = str(request.form.get("est_amount", None))
    title = str(request.form.get("title", None))
    expense_uuid = request.form.get("expense_uuid", None)

    if expense_type != "exp" and expense_type != "inc":
        return return_json(success=False, error="Invalid expense type: inc | exp")

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    if not data_validation.validate_amount(est_amount):
        return return_json(success=False, error="Est amount must be a number or decimal")

    return db.update_expense(user_uuid, expense_type, est_amount, title, expense_uuid)


@expenses_blueprint.route(expenses_prefix + "/update_current", methods=["POST"])
def update_current():
    user_uuid = str(request.form.get("uuid", None))
    expense_uuid = request.form.get("expense_uuid", None)
    amount = request.form.get("amount", None)

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    if amount is None:
        return return_json(success=False, error="Amount must be set")

    if not data_validation.validate_amount(amount):
        return return_json(success=False, error="Est amount must be a number or decimal")

    return db.update_current_value(user_uuid, expense_uuid, amount)


@expenses_blueprint.route(expenses_prefix + "/get", methods=["POST"])
def get_inc():
    user_uuid = str(request.form.get("uuid", None))

    if not data_validation.validate_uuid(user_uuid):
        return return_json(success=False, error="Invalid user UUID")

    if not data_validation.verify_user(user_uuid):
        return return_json(success=False, error="User not found")

    return db.get_user_expenses(user_uuid)


@expenses_blueprint.route(expenses_prefix + "/delete", methods=["POST"])
def delete_expense():
    user_uuid = request.form.get("uuid", None)
    expense_uuid = request.form.get("expense_uuid", None)
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

    return db.delete_expense(user_uuid, delete_all, expense_uuid)
