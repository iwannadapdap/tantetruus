from databases.db_handler import DBHandler
from models.recipe import Recipe
from returns import return_json


class Food_db(DBHandler):
    def __init__(self):
        super().__init__("recipes")

    def add_recipe(self, title: str, prep_time: int, ingredients: list, preperation: list):
        for item in ingredients:
            item.capitalize()
        for item in preperation:
            item.capitalize()

        new_recipe = Recipe(title, prep_time, ingredients, preperation)
        self.insert_one(new_recipe.json())
        return return_json(success=True)

    def update_recipe(self, uuid: str, title: str, prep_time: int, ingredients: list, preperation: list):
        res = self.find_one({'recipe_uuid': uuid})

        if not res:
            return return_json(success=False, error="recipe not found")

        c_recipe = Recipe()

        c_recipe.from_mongo(res)

        c_recipe.title = title
        c_recipe.prep_time = prep_time
        c_recipe.ingredients = ingredients

        for item in c_recipe.ingredients:
            item.capitalize()

        c_recipe.preperation = preperation

        for item in c_recipe.preperation:
            item.capitalize()

        self.update_one({'recipe_uuid': uuid}, {"$set": c_recipe.json()})

    def get_recipes(self):
        recipes = self.find_all()

        r_recipes = []
        for l_recipe in recipes:
            new_recipe = Recipe()
            new_recipe.from_mongo(l_recipe)
            r_recipes.append(new_recipe.json())

        return r_recipes

    def get_recipe(self, uuid):
        res = self.find_one({'recipe_uuid': uuid})

        if not res:
            return False

        c_recipe = Recipe()
        c_recipe.from_mongo(res)
        return c_recipe
