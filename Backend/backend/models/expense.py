from uuid import uuid4


class Expense(object):
    def __init__(self, title=None, expense_type=None, est_amount=None):
        self.expense_uuid = str(uuid4())
        self.title = title
        self.expense_type = expense_type
        self.est_amount = est_amount
        self.cur_amount = 0

    def from_mongo(self, mongo_data: dict):
        self.expense_uuid = mongo_data['expense_uuid']
        self.title = mongo_data['title']
        self.expense_type = mongo_data['expense_type']
        self.est_amount = mongo_data['est_amount']
        self.cur_amount = mongo_data['cur_amount']

    def json(self):
        return {
            'expense_uuid': self.expense_uuid,
            'title': self.title,
            'expense_type': self.expense_type,
            'est_amount': self.est_amount,
            'cur_amount': self.cur_amount
        }
