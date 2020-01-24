from flask import Blueprint, request, render_template, json

from databases import food_db

import data_validation

from returns import return_json

food_blueprint = Blueprint("food_blueprint", __name__)
food_prefix = "/food"

db = food_db.Food_db()


@food_blueprint.route(food_prefix + "/get", methods=["GET"])
def get_recipes():
    return return_json(success=True, data={'recipes': db.get_recipes()})


@food_blueprint.route(food_prefix + "/update", methods=["POST"])
def update_recipe():
    request_json = request.json
    if request_json["title"] is None:
        return return_json(succes=False, error="Title is not set")
    if request_json["prep_time"] is None:
        return return_json(succes=False, error="prep_time is not set")
    if request_json["ingredients"] is None:
        return return_json(succes=False, error="ingredients is not set")
    if request_json["preperation"] is None:
        return return_json(succes=False, error="preperation is not set")

    if 'uuid' in request_json:
        uuid = request_json["uuid"]
    else:
        uuid = None

    title = request_json["title"]
    prep_time = request_json["prep_time"]
    ingredients = request_json["ingredients"]
    preperation = request_json["preperation"]

    if not data_validation.validate_amount(prep_time):
        return return_json(success=False, error="prep_time must be an integer")

    if type(ingredients) != list:
        return return_json(success=False, error="Ingredients must be a list")

    if type(preperation) != list:
        return return_json(success=False, error="preperation must be a list")

    if uuid is not None:
        if not data_validation.validate_uuid(uuid):
            return return_json(success=False, error="Invalid uuid format")

        return db.update_recipe(uuid, title, prep_time, ingredients, preperation)
    return db.add_recipe(title, prep_time, ingredients, preperation)
