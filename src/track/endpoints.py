from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from .schema import Track, Track_Pydantic, TrackUpdate
from src.user.serializers import User_Pydantic
from src.user.jwt_auth import get_current_active_user
from src.genre.models import Genre

from .services import upload_track_to_s3


track_router = APIRouter()


@track_router.post("/tracks/")
async def create(
        song: UploadFile = File(...),
        name: str = None,
        track_author: str = None,
        text: str = None,
        is_hidden: bool = None,
        genre: list[int] = None,
        user: User_Pydantic = Depends(get_current_active_user)
):
    """ Create a track """
    if song.filename[-3:] == 'mp3':
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid track extension. Try to upload .mp3")
    track_path = 'track/' + f'user_{user.id}/' + song.filename
    track_s3_path = await upload_track_to_s3(song, track_path)
    track = await Track.create(
        name=name, track_author=track_author, owner_id=user.id, text=text, is_hidden=is_hidden, song=track_s3_path)
    genre = await Genre.filter(id__in=genre)
    await track.genre.add(*genre)
    return await Track_Pydantic.from_tortoise_orm(track)


@track_router.get("/tracks/", response_model=list[Track_Pydantic])
async def list():
    """ Return the list of all tracks """
    return await Track.filter(is_hidden=False).prefetch_related('genre', 'owner')


@track_router.get("/tracks/{track_id}", response_model=Track_Pydantic)
async def retrieve(track_id: int):
    """ Return the target track """
    return await Track.get(id=track_id).prefetch_related('genre', 'owner')


@track_router.get("/users/tracks/", response_model=Track_Pydantic)
async def owners_track_list(current_user: User_Pydantic = Depends(get_current_active_user)):
    """ Return the owner's track list """
    return await Track.filter(owner=current_user.id).prefetch_related('genre', 'owner')


@track_router.put("/users/track/{track_id}", response_model=Track_Pydantic)
async def owners_track_update(
        track_id: int, track: TrackUpdate,
        genre: List[int], current_user: User_Pydantic = Depends(get_current_active_user)):
    """ Return the owner's track list """
    track_obj = await Track.get(id=track_id)
    if track_obj.owner.id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only track's author can modify")
    await Track.filter(id=track_id).update(**track.dict(exclude_unset=True))
    genre_obj = await Genre.filter(id__in=genre)
    await track_obj.genre.clear()
    await track_obj.genre.add(*genre_obj)
    return await Track_Pydantic.from_queryset_single(Track.get(id=track_id))


@track_router.delete("/users/track/{track_id}", status_code=204)
async def owners_track_list(track_id: int, current_user: User_Pydantic = Depends(get_current_active_user)):
    """ Return the owner's track list """
    track = await Track.filter(id=track_id).first()
    if track.owner_id != current_user.id:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only track's author can delete the instance")
    if track.exists():
        return await track.delete()
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The track with this id does not exist")
