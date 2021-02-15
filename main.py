# Hi :)
from fastapi import FastAPI, Depends
from felp.sql import db, db_state_default
from felp.models import MODELS
import felp.schemas as schemas

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
    return "a"

@app.get("/meals", response_model=schemas.Meal, dependencies=[Depends(get_db)])
async def meals():
    return users