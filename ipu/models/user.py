from . import BaseModel
from ipu.sql import PeeweeGetterDict
from typing import List, Optional
from peewee import TextField
from pydantic import BaseModel as PydanticBaseModel
import os


@BaseModel.register
class User(BaseModel):
    first_name = TextField()
    last_name = TextField(null=True)
    email = TextField(null=True)
    username = TextField()
    password = TextField()

    class Settings(PydanticBaseModel):
        authjwt_secret_key: str = os.getenv("SECRET") or "indev"

    class UserBase(PydanticBaseModel):  # Our user.
        first_name: str
        last_name: Optional[str]
        email: Optional[str]
        username: str

    class UserAuth(UserBase):
        password: str  # This is only needed at create and login time
