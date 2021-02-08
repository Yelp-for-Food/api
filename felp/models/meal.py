from . import BaseModel
from peewee import CharField

@BaseModel.register
class Meal(BaseModel):
    name = CharField()
    category = CharField()
    area = CharField()
    thumb = CharField()