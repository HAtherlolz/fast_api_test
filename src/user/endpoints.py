from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from .models import User
from .serializers import User_Pydantic, Token, CreateUser, UserSerializer, UserIn_Pydantic
from .jwt_auth import get_password_hash, authenticate_user, create_access_token, get_current_active_user
from config.config import Settings

settings = Settings()
router_user = APIRouter()


@router_user.post("/users/create/")
async def create_user(form_data: CreateUser = Depends()):
    """ Create an user with a hashed password"""
    hashed_password = get_password_hash(form_data.password)
    user_obj = await User.create(email=form_data.email, password=hashed_password, is_active=True)
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router_user.get("/users/")
async def get_list_of_users():
    """ Returns a list of all users """
    return await User_Pydantic.from_queryset(User.all())


@router_user.get('/users/{user_id}')
async def get_target_user(user_id: int):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@router_user.get("/users/me/", response_model=User_Pydantic)
async def users_me(current_user: UserSerializer = Depends(get_current_active_user)):
    return current_user


@router_user.put('/user/update/', response_model=User_Pydantic)
async def update_user(user_data: UserSerializer, user: UserSerializer = Depends(get_current_active_user)):
    await User.filter(id=user.id).update(**user_data.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user.id))


@router_user.delete('/user/delete/', status_code=204)
async def delete_user(user: UserSerializer = Depends(get_current_active_user)):
    return await User.filter(id=user.id).delete()


@router_user.post("/token", response_model=Token)
async def login_for_access_token(form_data: CreateUser = Depends()):
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @app.post("/cities")
# async def create_city(file: UploadFile = File(...),
#                       name: str = Form(...)):
#     with open(f'media/{file.filename}', "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#         file = f'media/{file.filename}'
#         timezone = datetime.now()
#         response = {
#             'name': name,
#             'file': file,
#             'timezone': timezone
#         }
#         await City.create(name=name, file=file, timezone=timezone)
#         return response