from datetime import datetime


class HygieneItem():
    def __init__(self, name: str, last_time: datetime, frequency: int, task_done: bool):
        self.name = name
        self.last_time = last_time
        self.frequency = frequency
        self.send = None
        self.task_done = task_done

    @classmethod
    def from_mongo(cls, mongo_data: dict):
        return cls(mongo_data['name'],
                   mongo_data['last_time'],
                   mongo_data['frequency'],
                   mongo_data['task_done'],)

    def change_hygiene_to_done(self):
        self.last_time = datetime.today()
        self.task_done = True

    def change_hygiene_to_false(self):
        self.task_done = False

    def update_frequency(self, frequency: int):
        self.frequency = frequency

    def check_if_done(self):
        current_time = datetime.today()
        elapsed_seconds = (current_time - self.last_time).total_seconds()
        try:
            elapsed_seconds_since_last_notification = (
                current_time - self.send).total_seconds()
        except TypeError:
            elapsed_seconds_since_last_notification = 0
        # Convert seconds to days
        elapsed_days = int(divmod(elapsed_seconds, 86400)[0])
        print(type(elapsed_days))
        if elapsed_days > int(self.frequency) or self.task_done is False and \
                (elapsed_seconds_since_last_notification is None or elapsed_seconds_since_last_notification <= 86400):
            self.task_done = False
            return False
        return True

    def json(self):
        return {
            'name': self.name,
            'last_time': self.last_time,
            'frequency': self.frequency,
            'task_done': self.task_done,
        }
