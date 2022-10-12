from fastapi import FastAPI
from database import setup_database
from serializers import City_Pydantic, CityIn_Pydantic, User_Pydantic, UserIn_Pydantic
from models import City, User

app = FastAPI()

setup_database(app)


@app.get("/cities")
async def get_cities():
    return await City_Pydantic.from_queryset(City.all())


@app.post("/cities")
async def create_city(city: CityIn_Pydantic):
    city_obj = await City.create(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_tortoise_orm(city_obj)


@app.get('/cities/{city_id}')
async def get_target_city(city_id: int):
    return await City_Pydantic.from_queryset_single(City.get(id=city_id))


@app.delete('/cities/{city_id}')
async def get_target_city(city_id: int):
    await City.filter(id=city_id).delete()
    return {}


@app.get("/users")
async def get_user():
    return await User_Pydantic.from_queryset(User.all())


@app.post("/users")
async def create_user(user: UserIn_Pydantic):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get('/user/{user_id}')
async def get_target_city(user_id: int):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@app.delete('/user/{user_id}')
async def get_target_city(user_id: int):
    await User.filter(id=user_id).delete()
    return {}
