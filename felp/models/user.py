from . import BaseModel, PeeweeGetterDict
from .meal import Meal
from typing import List
from peewee import TextField, JSONField
from pydantic import BaseModel as PydanticBaseModel

@BaseModel.register
class User(BaseModel):
    first_name = TextField()
    last_name = TextField(null=True)
    email = TextField(null=True)
    username = TextField()
    password = TextField() # TODO: What else does a user need?
    liked_meals = JSONField(default={})

    class _UserBase(PydanticBaseModel): # Our user.
        email: str

    class UserCreate(_UserBase):
        password: str # This is only needed at create time, so who cares!

    class UserSchema(_UserBase):
        id: int # Peeweee makes this
        is_active: bool
        liked_meals: List[Meal.MealSchema] = []

        class Config:
            orm_mode = True
            getter_dict = PeeweeGetterDict