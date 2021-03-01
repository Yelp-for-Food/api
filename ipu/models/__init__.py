from peewee import Model
from ipu.sql import db

MODELS = []


class BaseModel(Model):
    class Meta:
        database = db

    @staticmethod
    def register(cls):
        MODELS.append(cls)
        return cls