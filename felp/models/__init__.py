from peewee import Model
from felp.sql import db

MODELS = []

class BaseModel(Model):

    class Meta:
        database = db

    @staticmethod
    def register(cls):
        MODELS.append(cls)
        return cls