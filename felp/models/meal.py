from . import BaseModel
from felp.sql import PeeweeGetterDict
from peewee import TextField
from pydantic import BaseModel as PydanticBaseModel


@BaseModel.register
class Meal(BaseModel):
    name = TextField()
    category = TextField()
    area = TextField()
    thumb = TextField()

    @staticmethod
    def get_meal(meal_id):
        # Meal.get(Meal.name == "name")
        # Meal.get_by_id(id)
        return Meal.get_by_id(meal_id)

    @staticmethod
    def get_all_meals():
        return Meal.select().iterator()

    @staticmethod
    def get_meal_by_name(name: str):
        return Meal.select().where(Meal.name.contains(name))

    @staticmethod
    def change_meal(meal_id: int, **data):
        return Meal.get_by_id(meal_id).update(data)

    class _MealBase(PydanticBaseModel):  # The thing, internally.
        name: str
        category: str
        area: str
        thumb: str

        class Config:
            orm_mode = True

        # getter_dict = (
        #    PeeweeGetterDict  # Does some magic to turn lists into.. nothing.
        # )

    class MealCreate(_MealBase):  # The thing, but what it takes to make it
        pass

    class MealSchema(_MealBase):  # The thing, but what is returned
        name: str
        category: str
        area: str
        thumb: str
        id: int
