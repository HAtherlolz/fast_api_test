from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form

from .schemas import PlayListOut, PlayList_Pydantic, PlayListIn_Pydantic, PlayListUpdate

from src.user.serializers import User_Pydantic
from src.user.jwt_auth import get_current_active_user

from src.track.models import Track

from .models import PlayList
from .services import upload_playlist_poster_to_s3, delete_file_to_s3

playlist_router = APIRouter()


@playlist_router.post("/playlist/", response_model=PlayListOut)
async def create_playlist(
        name: str = Form(...),
        description: str = Form(...),
        poster: UploadFile = File(...),
        is_hidden: bool = Form(...),
        track: list[int] = Form(None),
        owner: User_Pydantic = Depends(get_current_active_user)
):
    """ Create a playlist """
    allowed_extensions = ["png", "jpg", "jpeg"]
    poster_extension = poster.filename.split('.')
    if not poster_extension[1] in allowed_extensions:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid posters extension. Try to upload .png, .jpg, or jpeg"
        )
    playlist_poster_path = 'playlist/poster/' + f'{name}/' + poster.filename
    playlist_poster = await upload_playlist_poster_to_s3(poster, playlist_poster_path)
    play_list = await PlayList.create(
        name=name, description=description, poster=playlist_poster, is_hidden=is_hidden, owner_id=owner.id
    )

    if track is not None:
        tracks = await Track.filter(id__in=track)
        for track in tracks:
            track_owner = await track.owner
            if track_owner == owner:
                await play_list.track.add(track)
            else:
                if not track.is_hidden:
                    await play_list.track.add(track)
    return await PlayList_Pydantic.from_tortoise_orm(play_list)


@playlist_router.get("/playlists/", response_model=List[PlayListOut])
async def get_list_of_playlists():
    """ Get lists of all not hidden playlists """
    return await PlayList_Pydantic.from_queryset(
        PlayList.filter(is_hidden=False)
    )


@playlist_router.get("/playlist/{playlist_id}", response_model=PlayListOut)
async def get_retrieve_play_list(playlist_id: int):
    """ Get target playlist by id """
    return await PlayList_Pydantic.from_tortoise_orm(
        await PlayList.get(id=playlist_id)
    )


@playlist_router.get("/user/playlists/", response_model=List[PlayListOut])
async def owners_playlists_list(current_user: User_Pydantic = Depends(get_current_active_user)):
    """ Return the owner's playlists list """
    return await PlayList_Pydantic.from_queryset(
        PlayList.filter(owner=current_user)
    )


@playlist_router.put("/user/playlist/{playlist_id}", response_model=PlayListOut)
async def update_play_list(
        playlist_id: int,
        playlist: PlayListUpdate,
        tracks: List[int],
        current_user: User_Pydantic = Depends(get_current_active_user)
):
    playlist_obj = await PlayList.get(id=playlist_id)
    play_list_owner = await playlist_obj.owner
    if play_list_owner.id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the playlist's author can modify")
    await PlayList.filter(id=playlist_id).update(**playlist.dict(exclude_unset=True))
    tracks_objs = await Track.filter(id__in=tracks)
    await playlist_obj.track.clear()
    await playlist_obj.track.add(*tracks_objs)
    return await PlayList_Pydantic.from_queryset_single(PlayList.get(id=playlist_id))


@playlist_router.put("/user/playlist/{playlist_id}/poster/", response_model=PlayListOut)
async def update_play_list_poster(
        playlist_id: int,
        poster: UploadFile = File(...),
        current_user: User_Pydantic = Depends(get_current_active_user)
):
    """ Update playlist poster by owner """
    allowed_extensions = ["png", "jpg", "jpeg"]
    poster_extension = poster.filename.split('.')
    if not poster_extension[1] in allowed_extensions:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid posters extension. Try to upload .png, .jpg, or jpeg"
        )
    playlist_obj = await PlayList.get(id=playlist_id)
    play_list_owner = await playlist_obj.owner
    if play_list_owner.id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the playlist's author can modify")
    await delete_file_to_s3(playlist_obj.poster)
    playlist_poster_path = 'playlist/poster/' + f'{playlist_obj.name}/' + poster.filename
    new_poster_path = await upload_playlist_poster_to_s3(poster, playlist_poster_path)
    await PlayList.filter(id=playlist_id).update(poster=new_poster_path)
    return await PlayList_Pydantic.from_queryset_single(PlayList.get(id=playlist_id))


@playlist_router.delete("/user/playlist/{playlist_id}")
async def destroy_playlist(playlist_id: int, current_user: User_Pydantic = Depends(get_current_active_user)):
    """ Delete the user playlists """
    playlist_obj = await PlayList.filter(id=playlist_id).first()
    if playlist_obj is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The playlist with this id does not exist")
    if playlist_obj.owner_id == current_user.id:
        await playlist_obj.delete()
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the playlist owner can delete the instance")
