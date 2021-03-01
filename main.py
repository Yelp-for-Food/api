# Hi :)
from fastapi import FastAPI, Depends, HTTPException
from ipu.sql import db, db_state_default
from ipu.models import MODELS
from ipu.models.meal import Meal
from typing import List

db.connect()
db.create_tables(MODELS)
db.close()

app = FastAPI()


async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()


@app.get("/")
async def root():
    return "Hello, World!"


@app.get("/meals", response_model=List[Meal.MealSchema], dependencies=[Depends(get_db)])
async def meals():
    return Meal.get_all_meals()


@app.get(
    "/meals/{meal_id}", response_model=Meal.MealSchema, dependencies=[Depends(get_db)]
)
async def meal_id(meal_id: int):
    meal = Meal.get_meal(meal_id)

    if meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    else:
        return meal
