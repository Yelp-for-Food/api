# Hi :)
from starlette.requests import Request
from starlette.responses import JSONResponse
from ipu.models.user import User
from fastapi import FastAPI, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from ipu.sql import db, db_state_default
from ipu.models.meal import Rating, Meal
from ipu.models import MODELS
from typing import List
import bcrypt

db.connect()
db.create_tables([Rating])
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


@AuthJWT.load_config
def get_config():
    return User.Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handle(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/")
async def root():
    return "Hello, World!"


@app.post("/login")
def login(user: User.UserAuth, Authorize: AuthJWT = Depends()):
    actual_user = User.get(username=user.username)
    if not bcrypt.checkpw(user.password, actual_user.password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}


@app.post("/signup")
def register(user: User.UserAuth, Authorize: AuthJWT = Depends()):
    User.create(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        password=bcrypt.hashpw(user.password, bcrypt.gensalt()),
    )


@app.get("/user")
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    return {"user": Authorize.get_jwt_subject()}


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


@app.get("/meals/{meal_id}/rating", dependencies=[Depends(get_db)])
async def get_rating_for_meal(meal_id: int):
    rating = Rating.get_rating_for(meal_id)

    if rating is None:
        raise HTTPException(status_code=404, detail="No Rating")
    else:
        return rating


@app.post("/meals/{meal_id}/rating", dependencies=[Depends(get_db)])
async def user_rate_meal(meal_id: int, rating: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    Rating.insert(user_id=current_user.id, meal_id=meal_id, rating=rating).execute()
    return "ok"  # TODO: Better response here.
