import string
import requests
import os, sys
from ipu.sql import db
from ipu.models import MODELS
from ipu.models.meal import Meal
from peewee import *


def create_tables():
    with db:
        db.create_tables(MODELS)


if not Meal.table_exists():
    create_tables()
elif os.getenv("FORCE") != "yes":
    meal = Meal.get(name="Corba")
    print("Cancelling execution to ensure data integrity. Pass FORCE to continue.")
    sys.exit()

BASE_URL = "https://www.themealdb.com/api/json/v1/1/search.php"

for letter in list(string.ascii_lowercase):
    query = {"f": letter}
    res = requests.request("GET", BASE_URL, params=query).json()["meals"]

    if res is None:
        continue  # gtfo

    for meal in res:
        Meal.create(
            name=meal["strMeal"],
            category=meal["strCategory"],
            area=meal["strArea"],
            thumb=meal["strMealThumb"],
        )
    print("Finished {}, continuing...".format(letter))

print("Task complete.")
