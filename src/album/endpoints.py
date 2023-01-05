from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form

from src.user.jwt_auth import get_current_active_user, User_Pydantic
from .schemas import Album, Album_Pydantic, AlbumUpdate, List_Album, AlbumRetrieve

from src.track.services import upload_track_to_s3

album_router = APIRouter()


@album_router.post("/albums/")
async def create(
        poster: UploadFile = File(...),
        name: str = File(...),
        description: str = File(...),
        is_hidden: bool = File(...),
        user: User_Pydantic = Depends(get_current_active_user)
):
    """ Create an album """
    allowed_extensions = ["png", "jpg", "jpeg"]
    poster_extension = poster.filename.split('.')
    if not poster_extension[1] in allowed_extensions:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid posters extension. Try to upload .png, .jpg, or jpeg"
        )
    album_poster_path = 'poster/' + f'{name}/' + poster.filename
    poster_s3_path = await upload_track_to_s3(poster, album_poster_path)
    album = await Album.create(
        name=name, description=description, owner_id=user.id, is_hidden=is_hidden, poster=poster_s3_path)
    return await Album_Pydantic.from_tortoise_orm(album)


@album_router.get("/albums/", response_model=list[List_Album])
async def list():
    """ Return the list of albums """
    return await Album.filter(is_hidden=False).prefetch_related("owner")


@album_router.get("/album/{album_id}", response_model=AlbumRetrieve)
async def retrieve(album_id: int):
    """ Return the target album """
    # print(await Album.get(id=album_id).prefetch_related('owner', 'track'))
    return await Album_Pydantic.from_tortoise_orm(await Album.get(id=album_id).prefetch_related('owner', 'track'))


@album_router.get("/users/albums/", response_model=List[List_Album])
async def owners_album_list(current_user: User_Pydantic = Depends(get_current_active_user)):
    """ Return the owner's albums list """
    return await Album.filter(owner=current_user.id).prefetch_related('owner')


@album_router.put("/users/album/{album_id}", response_model=AlbumRetrieve)
async def update_album(
        album_id: int,
        album_data: AlbumUpdate,
        current_user: User_Pydantic = Depends(get_current_active_user)
):
    """ Update album """
    album_obj = await Album.filter(id=album_id).first()
    if not album_obj.exists():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album with this id does not exist")
    if album_obj.owner_id == current_user.id:
        await Album.filter(id=album_id).update(**album_data.dict(exclude_unset=True))
        return await Album_Pydantic.from_tortoise_orm(await Album.get(id=album_id).prefetch_related('owner'))
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only album's author can delete the instance")


@album_router.delete("/users/albums/{album_id}", status_code=204)
async def destroy(album_id: int, current_user: User_Pydantic = Depends(get_current_active_user)):
    album_obj = await Album.filter(id=album_id).first()
    if not album_obj.exists():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album with this id does not exist")
    if album_obj.owner_id == current_user.id:
        await album_obj.delete()
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only albums author can delete the instance")