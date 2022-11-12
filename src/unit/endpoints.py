from fastapi import APIRouter, Depends, HTTPException, status
from .models import Unit
from .serializers import Unit_Pydantic,UnitMapIdLAtLngSerializer

router = APIRouter()


@router.get("/units/", response_model=UnitMapIdLAtLngSerializer)
async def get_lits_of_units():
    units = await Unit.get(id=1)

    print(units.lat)
    return await Unit.all()