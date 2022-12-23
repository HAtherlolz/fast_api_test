from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from config.config import Settings
from .models import User
from .serializers import User_Pydantic, Token, CreateUser, UserSerializer, UserIn_Pydantic, Uuid
from .jwt_auth import get_password_hash, authenticate_user, create_access_token, get_current_active_user
from .services import encode_uuid, decode_uuid


settings = Settings()
router_user = APIRouter()


@router_user.post("/users/create/")
async def create_user(user: CreateUser):
    """ Create an user with a hashed password"""
    hashed_password = get_password_hash(user.password)
    user_obj = await User.create(email=user.email, password=hashed_password, is_active=True)
    # uuid = await encode_uuid(str(user_obj.id))
    # await send_with_template(user_obj.email, uuid)
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


@router_user.post('/user/email/activation/', status_code=201, response_model=User_Pydantic)
async def email_ativation(uuid: Uuid):
    user_id = await decode_uuid(uuid.uuid)
    user = await User.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong uuid",)
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user is already activated", )
    user.is_active = True
    await user.save(update_fields=['is_active'])
    return await User_Pydantic.from_queryset_single(User.get(id=user.id))


@router_user.post("/token", response_model=Token)
async def login_for_access_token(user: CreateUser):
    user = await authenticate_user(user.email, user.password)
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