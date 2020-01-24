from datetime import datetime
from uuid import uuid4


class Recipe():
    def __init__(self, title: str = None, prep_time: int = None, ingredients: list = None, preperation: list = None):
        self.recipe_uuid = str(uuid4())
        self.title = title
        self.prep_time = prep_time
        self.ingredients = ingredients
        self.preperation = preperation
        self.created_at = datetime.now()

    def from_mongo(self, mongo_data: dict):
        self.recipe_uuid = mongo_data['recipe_uuid']
        self.title = mongo_data['title']
        self.prep_time = mongo_data['prep_time']
        self.ingredients = mongo_data['ingredients']
        self.preperation = mongo_data['preperation']
        self.created_at = mongo_data['created_at']

    def json(self):
        return {
            'recipe_uuid': self.recipe_uuid,
            'title': self.title,
            'prep_time': self.prep_time,
            'ingredients': self.ingredients,
            'preperation': self.preperation,
            'created_at': self.created_at
        }
