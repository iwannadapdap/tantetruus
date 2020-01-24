from databases.db_handler import DBHandler as db_handler
from models import user, expense, expenses
from returns import return_json
from data_validation import validate_uuid


class Expense_db(db_handler):
    def __init__(self):
        super().__init__("expenses")

    def create_expenses(self, user_uuid: str):
        self.insert_one(expenses.Expenses(user_uuid).json())

    def get_user_expenses(self, user_uuid: str):
        raw_expenses = self.find_one({'user_uuid': user_uuid})['expenses']
        r_incomes = []
        r_expenses = []
        cur_balance = 0
        est_balance = 0
        for c_expense in raw_expenses:
            if c_expense['expense_type'] == "inc":
                r_incomes.append(c_expense)
                cur_balance += float(c_expense['cur_amount'])
                est_balance += float(c_expense['est_amount'])
            else:
                r_incomes.append(c_expense)
                cur_balance -= float(c_expense['cur_amount'])
                est_balance -= float(c_expense['est_amount'])

        return return_json(success=True,
                           data={'incomes': r_incomes,
                                 'expenses': r_expenses,
                                 'cur_balance': str(cur_balance),
                                 'est_balance': str(est_balance)})

    def update_current_value(self, user_uuid: str, expense_uuid: str, amount: str):
        res = self.find_one({'user_uuid': user_uuid})

        for c_expense in res["expenses"]:
            if c_expense['expense_uuid'] == expense_uuid:
                if amount == "0":
                    c_expense['cur_amount'] = 0
                    self.update_one({'user_uuid': user_uuid},
                                    {"$set": res})
                    return return_json(success=True,
                                       data={"message": "Current amount cleared for {0}"
                                                        .format(c_expense['title'])})

                amount_to_add = float(amount)
                current_amount = float(c_expense['cur_amount'])
                c_expense['cur_amount'] = current_amount + amount_to_add
                self.update_one({'user_uuid': user_uuid}, {
                                "$set": res})

                return return_json(success=True,
                                   data={"message": "Current amount updated for {0}: {1}"
                                                    .format(c_expense['title'],
                                                            c_expense['cur_amount'])})

        return return_json(success=False,
                           error="Expense not found")

    def update_expense(self, user_uuid: str, expense_type, est_amount, title, expense_uuid=None):
        res = self.find_one({'user_uuid': user_uuid})

        if not res:
            return return_json(success=False, error="No expenses found")

        c_expenses = expenses.Expenses()
        c_expenses.from_mongo(res)

        if expense_uuid is None:
            res = c_expenses.add_expense(
                title, expense_type, est_amount)

            if not res[0]:
                return return_json(success=False,
                                   error="Fields are empty")

            self.update_one({'user_uuid': user_uuid}, {
                            "$set": c_expenses.json()})
            return return_json(success=True,
                               data={'message': "Expense added!"})

        if not validate_uuid(expense_uuid):
            return return_json(success=False,
                               error="Invalid expense UUID")

        res = c_expenses.update_expense(
            expense_uuid, expense.Expense(title, expense_type, est_amount))

        if res[0]:
            self.update_one({'user_uuid': user_uuid}, {
                            "$set": c_expenses.json()})
            return return_json(success=True,
                               data={'message': "Expense updated!"})
        return return_json(success=False,
                           error=res[1])

    def delete_expense(self, user_uuid: str, delete_all: bool, expense_uuid):
        res = self.find_one({'user_uuid': user_uuid})

        if not res:
            return return_json(success=False, error="No expenses found")

        c_expenses = expenses.Expenses()
        c_expenses.from_mongo(res)

        if delete_all and expense_uuid is None:
            c_expenses.delete_expense(delete_all=True)
            self.update_one({'user_uuid': user_uuid}, {
                            "$set": c_expenses.json()})
            return return_json(success=True, data={'message': 'all expenses were deleted'})

        elif not delete_all and expense_uuid is not None:
            if not validate_uuid(expense_uuid):
                return return_json(success=False, error="Invalid expense UUID")

            c_expenses.delete_expense(_expense_uuid=expense_uuid)
            self.update_one({'user_uuid': user_uuid}, {
                            "$set": c_expenses.json()})
            return return_json(success=True, data={'message': 'one expense was deleted'})
        else:
            return return_json(success=False, error="delete_all & expense uuid can't both be set")
