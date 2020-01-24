import pymongo

import app_config


class DBHandler(object):
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(app_config.MONGO_URL)
        self.collection_name = collection_name
        self.collection = self.client["tanteTruus"][collection_name]

    def find_all(self):
        return self.collection.find({}, {'_id': 0})

    def find_one(self, query: dict):
        return self.collection.find_one(query, {'_id': 0})

    def drop_all(self):
        return self.client.drop_database('tanteTruus')

    def drop_coll(self):
        try:
            self.collection.drop()
            return True
        except Exception as e:
            return string(e)

    def insert_one(self, data: dict):
        try:
            self.collection.insert_one(data)
            return True
        except Exception as e:
            return str(e)

    def update_one(self, query: dict, data: dict):
        return self.collection.update_one(query, data)

    def delete_one(self, querry: dict):
        return self.collection.remove(querry)
