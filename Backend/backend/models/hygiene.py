from datetime import datetime
from returns import return_json
from models.hygiene_item import HygieneItem


class Hygiene():
    def __init__(self, user_uuid: str = None):
        self.user_uuid = user_uuid
        self._hygiene = [
            HygieneItem("sheets", datetime.today(), 7, True),
            HygieneItem("bathroom", datetime.today(), 14, True),
            HygieneItem("house", datetime.today(), 21, True,),
            HygieneItem("kitchen", datetime.today(), 7, True),
            HygieneItem("dishes", datetime.today(), 3, True),
            HygieneItem("vacuum", datetime.today(), 7, True)
        ]

    def from_mongo(self, mongo_data: dict):
        self.user_uuid = mongo_data["user_uuid"]
        self._hygiene.clear()
        for item in mongo_data["hygiene"]:
            self._hygiene.append(HygieneItem.from_mongo(item))

    def check_hygiene(self):
        not_done = []
        for item in self._hygiene:
            if not item.check_if_done():
                not_done.append(item)
                item.send = datetime.now()
        return not_done

    def update_hygiene(self, name: str, done: bool):
        for item in self._hygiene:
            if item.name == name:
                if done:
                    item.change_hygiene_to_done()
                    return return_json(success=True, data={"message": "Item {0} was set to done".format(item.name)})
                # Set back to not done
                item.change_hygiene_to_false()
                return return_json(success=True, data={"message": "Item {0} was set to not done".format(item.name)})

        return return_json(success=False, error="No hygiene item found with name {0}".format(name))

    def update_notifiations(self, notifications: dict):
        for item in self._hygiene:
            item.update_frequency(notifications[item.name])

        return True

    def json(self):
        json_list = []
        for item in self._hygiene:
            json_list.append(item.json())
        return {
            'user_uuid': self.user_uuid,
            'hygiene': json_list
        }
