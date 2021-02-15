from . import BaseModel, PeeweeGetterDict
from peewee import TextField
from pydantic import BaseModel as PydanticBaseModel

@BaseModel.register
class Meal(BaseModel):
    name = TextField()
    category = TextField()
    area = TextField()
    thumb = TextField()

    class _MealBase(PydanticBaseModel): # The thing, internally.
        name: str
        category: str
        area: str
        thumb: str
        
    class MealCreate(_MealBase): # The thing, but what it takes to make it
        pass
    
    class MealSchema(_MealBase): # The thing, but what is returned
        id: int
        
        class Config:
            orm_mode = True
            getter_dict = PeeweeGetterDict # Does some magic to turn lists into.. nothing.