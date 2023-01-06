from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form

from .schema import Track, Track_Pydantic, TrackUpdate, TrackOut
from src.user.serializers import User_Pydantic
from src.user.jwt_auth import get_current_active_user
from src.genre.models import Genre

from .services import track_poster_create


track_router = APIRouter()


@track_router.post("/tracks/", response_model=TrackOut)
async def create(
        song: UploadFile = File(...),
        song_poster: UploadFile = File(...),
        name: str = Form(...),
        track_author: str = Form(...),
        text: str = Form(...),
        is_hidden: bool = Form(...),
        album_id: int = Form(default=None),
        genre: list[int] = Form(...),
        user: User_Pydantic = Depends(get_current_active_user)
):
    """ Create a track """
    if not song.filename.split('.')[1] == 'mp3':
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid track extension. Try to upload .mp3")
    track_s3_path, tracks_poster_s3_path = await track_poster_create(user.id, song, song_poster)
    track = await Track.create(
        name=name, track_author=track_author, owner_id=user.id,
        text=text, is_hidden=is_hidden, song=track_s3_path,
        song_poster=tracks_poster_s3_path, album_id=album_id
    )
    genre = await Genre.filter(id__in=genre)
    await track.genre.add(*genre)
    return await Track_Pydantic.from_tortoise_orm(track)


@track_router.get("/tracks/", response_model=list[TrackOut])
async def list():
    """ Return the list of all tracks """
    return await Track_Pydantic.from_queryset(
        Track.filter(is_hidden=False).prefetch_related('genre', 'owner', 'album').order_by('-views_count')
    )


@track_router.get("/tracks/{track_id}", response_model=TrackOut)
async def retrieve(track_id: int):
    """ Return the target track """
    track_obj = await Track.get(id=track_id)
    track_obj.views_count += 1
    await track_obj.save()
    return await Track_Pydantic.from_queryset_single(Track.get(id=track_id).prefetch_related('genre', 'owner', 'album'))


@track_router.get("/users/tracks/", response_model=List[TrackOut])
async def owners_track_list(current_user: User_Pydantic = Depends(get_current_active_user)):
    """ Return the owner's track list """
    return await Track_Pydantic.from_queryset(
        Track.filter(owner=current_user.id).prefetch_related('genre', 'owner', 'album').order_by('-views_count')
    )


@track_router.put("/users/track/{track_id}", response_model=TrackOut)
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
async def destroy(track_id: int, current_user: User_Pydantic = Depends(get_current_active_user)):
    """ Return the owner's track list """
    track = await Track.filter(id=track_id).first()
    if track.owner_id != current_user.id:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only track's author can delete the instance")
    if track.exists():
        return await track.delete()
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The track with this id does not exist")
