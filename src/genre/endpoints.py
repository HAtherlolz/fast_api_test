from fastapi import APIRouter

from .schema import Genre, Genre_Pydantic, GenreIn_Pydantic, GenreOut


genre_router = APIRouter()


@genre_router.post("/genre/", response_model=GenreOut)
async def create_genre(genre: GenreIn_Pydantic):
    """ Create a song genre """
    return await Genre.create(**genre.dict())


@genre_router.get("/genre/", response_model=list[GenreOut])
async def list():
    """ Get all genres """
    return await Genre.all()


@genre_router.get("/genre/{genre_id}", response_model=GenreOut)
async def retrieve(genre_id: int):
    """ Get target genre """
    return await Genre.get(id=genre_id)


@genre_router.put("/genre/{genre_id}", response_model=GenreOut)
async def update(genre_id: int, genre: GenreIn_Pydantic):
    """ Update target genre """
    await Genre.filter(id=genre_id).update(**genre.dict())
    return await Genre_Pydantic.from_queryset_single(Genre.get(id=genre_id))


@genre_router.delete("/genre/{genre_id}", status_code=204)
async def destroy(genre_id: int):
    """ Delete target genre """
    return await Genre.filter(id=genre_id).delete()
