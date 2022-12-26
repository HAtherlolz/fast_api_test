from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from config.config import Settings
from .models import User
from .serializers import User_Pydantic, Token, CreateUser, UserSerializer, UserIn_Pydantic, EmailActivationToken
from .jwt_auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_user
)
from .services import upload_file_to_s3, delete_file_to_s3, send_test_email, get_jwt


settings = Settings()
router_user = APIRouter()


@router_user.post("/users/create/")
async def create_user(user: CreateUser):
    """ Create an user with a hashed password"""
    hashed_password = get_password_hash(user.password)
    user_obj = await User.create(
        email=user.email, password=hashed_password, is_active=False, avatar=settings.AWS_BUCKET_DEFAULT_AVATAR_PATH
    )
    access_token = await get_jwt(user_obj)
    send_test_email(user_obj.email, access_token)
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router_user.get("/users/")
async def get_list_of_users():
    """ Returns a list of all users """
    return await User_Pydantic.from_queryset(User.all())


@router_user.get('/users/{user_id}')
async def get_target_user(user_id: int):
    """ Get user id and return target user's data """
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@router_user.get("/users/me/", response_model=User_Pydantic)
async def users_me(current_user: UserSerializer = Depends(get_current_active_user)):
    """ get jwt token in header and return current user's data """
    return current_user


@router_user.put('/user/update/', response_model=User_Pydantic)
async def update_user(user_data: UserSerializer, user: UserSerializer = Depends(get_current_active_user)):
    """ Update user's data """
    await User.filter(id=user.id).update(**user_data.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user.id))


@router_user.put('/user/update/avatar/', response_model=User_Pydantic)
async def update_user_avatar(file: UploadFile = File(...), user: UserSerializer = Depends(get_current_active_user)):
    """ Update user's avatar with formdata """
    image_path = 'avatars/' + f'user_{user.id}/' + file.filename
    if user.avatar != settings.AWS_BUCKET_DEFAULT_AVATAR_PATH and user.avatar is not None:
        await delete_file_to_s3(user.avatar)
    user.avatar = await upload_file_to_s3(file, image_path)
    await user.save(update_fields=['avatar'])
    return await User_Pydantic.from_queryset_single(User.get(id=user.id))


@router_user.delete('/user/delete/', status_code=204)
async def delete_user(user: UserSerializer = Depends(get_current_active_user)):
    """ Delete user's owner account """
    return await User.filter(id=user.id).delete()


@router_user.delete('/user/{user_id}/delete/', status_code=204)
async def delete_user(user_id: int):
    """ Endpoint only for fast deleting users """
    return await User.filter(id=user_id).delete()


@router_user.post('/user/email/activation/', status_code=201, response_model=Token)
async def email_ativation(token: EmailActivationToken):
    """ Make user active and return jwt token """
    user = await get_current_user(token.token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong token")
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user is already activated")
    user.is_active = True
    await user.save(update_fields=['is_active'])
    access_token = await get_jwt(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router_user.post("/token", response_model=Token)
async def login_for_access_token(user: CreateUser):
    """ Check user's log pass if data is valid and user is_active return jwt token """
    user = await authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active",
        )
    access_token = await get_jwt(user)
    return {"access_token": access_token, "token_type": "bearer"}
