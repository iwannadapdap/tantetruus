from models.expense import Expense


class Expenses(object):
    def __init__(self, user_uuid: str = None, expenses: list = None):
        self.user_uuid = user_uuid
        if expenses is not None:
            self._expenses = expenses
        else:
            self._expenses = []

    def add_expense(self, name: str = None, expense_type: str = None, amount: str = None):
        if name is None or expense_type is None or amount is None:
            return [False, "Need name, expense_type and amount"]
        new_expense = Expense(name, expense_type, amount)
        self._expenses.append(new_expense.json())
        return [True, "User added"]

    def update_expense(self, expense_uuid, new_expense):
        i = 0
        for idx, l_expense in enumerate(self._expenses):
            if 'expense_uuid' in l_expense:
                c_expense = Expense()
                c_expense.from_mongo(l_expense)
                if c_expense.expense_uuid == expense_uuid:
                    self._expenses[idx] = new_expense.json()
                    return [True, "expense found and updated"]
            i += 1
        return [False, "expense not found"]

    def delete_expense(self, _expense_uuid=None, delete_all: bool = False):
        i = 0
        if delete_all:
            self._expenses = []
            return [True, "deleted all events"]

        for idx, l_expense in enumerate(self._expenses):
            if 'expense_uuid' in l_expense:
                c_expense = Expense()
                c_expense.from_mongo(l_expense)
                if c_expense.expense_uuid == _expense_uuid:
                    del self._expenses[idx]
                    return [True, "expense found and deleted"]
            i += 1
        return [False, "expense not found"]

    def from_mongo(self, mongo_data: dict):
        self.user_uuid = mongo_data["user_uuid"]
        self._expenses = mongo_data["expenses"]

    def json(self):
        return {
            'user_uuid': self.user_uuid,
            'expenses': self._expenses
        }
