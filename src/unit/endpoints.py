from fastapi import APIRouter, Depends, HTTPException, status
from .models import Unit
from .serializers import Unit_Pydantic,UnitMapIdLAtLngSerializer, ListUnitMapIdLAtLngSerializer

router = APIRouter()


@router.get("/units/", response_model=ListUnitMapIdLAtLngSerializer)
async def get_lits_of_units():
    units = await Unit.all()

    print(units)
    return await Unit.all()