from . import BaseModel
from ipu.sql import PeeweeGetterDict
from ipu.models.user import User
from peewee import Check, ForeignKeyField, IntegerField, TextField, fn
from pydantic import BaseModel as PydanticBaseModel

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut sem viverra aliquet eget. Justo donec enim diam vulputate ut pharetra sit amet aliquam. Neque egestas congue quisque egestas diam in arcu. Erat imperdiet sed euismod nisi porta lorem mollis aliquam ut. Elementum pulvinar etiam non quam lacus suspendisse faucibus interdum posuere. Blandit cursus risus at ultrices mi tempus imperdiet nulla malesuada. Nunc mi ipsum faucibus vitae aliquet nec ullamcorper sit amet. Malesuada nunc vel risus commodo. Sagittis purus sit amet volutpat consequat mauris. Tellus id interdum velit laoreet id. Ut pharetra sit amet aliquam id diam maecenas ultricies mi. Scelerisque mauris pellentesque pulvinar pellentesque habitant morbi. Sit amet mattis vulputate enim. Pellentesque sit amet porttitor eget dolor morbi non arcu risus. Nullam vehicula ipsum a arcu cursus vitae congue. Vestibulum morbi blandit cursus risus at ultrices mi tempus imperdiet. In pellentesque massa placerat duis ultricies lacus sed. Netus et malesuada fames ac turpis egestas."


@BaseModel.register
class Meal(BaseModel):
    name = TextField()
    category = TextField()
    area = TextField()
    thumb = TextField()
    description = LOREM_IPSUM

    @staticmethod
    def get_meal(meal_id):
        # Meal.get(Meal.name == "name")
        # Meal.get_by_id(id)
        return Meal.get_by_id(meal_id)

    @staticmethod
    def get_all_meals():
        return list(Meal.select())

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
        description: str

        class Config:
            orm_mode = True

        # getter_dict = (
        #    PeeweeGetterDict  # Does some magic to turn lists into.. nothing.
        # )

    class MealCreate(_MealBase):  # The thing, but what it takes to make it
        pass

    class MealSchema(_MealBase):  # The thing, but what is returned
        id: int


@BaseModel.register
class Rating(BaseModel):
    user_id = ForeignKeyField(User, backref="user_ratings")
    meal_id = ForeignKeyField(Meal, backref="user_ratings")
    rating = IntegerField(constraints=[Check("rating <= 5")])

    @staticmethod
    def get_rating_for(meal: int):
        return Rating.select().where(Rating.meal_id == meal)

    class _RatingBase(PydanticBaseModel):
        user_id: int
        data_id: int
        rating: int

    class RatingSchema(_RatingBase):
        id: int  # Peeweee makes this

        class Config:
            orm_mode = True