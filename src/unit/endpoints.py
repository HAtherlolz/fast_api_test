from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, status, Request
from tortoise.expressions import Q

from .models import Unit
from .serializers import Unit_Pydantic, UnitMapIdLAtLngSerializer, ListUnitMapIdLAtLngSerializer

router = APIRouter()


#response_model=ListUnitMapIdLAtLngSerializer


@router.get("/units/", response_model=ListUnitMapIdLAtLngSerializer)
async def get_lits_of_units(
        region: str = None,
        search: str = None,
        sort_price: str = None,
        category: str = None,
        model_name: str = None,
        manufacturers: str = None,
        services: str = None,
        name: str = None
):

    units = Unit.filter(is_approved=True)
    if region is not None and len(region) > 0:
        print(region)
        regions = region.split(',')
        print(regions)
        units = units.filter(region__in=regions).distinct()
        print(type(units))
    else:
        units = Unit.all()

    if search is not None and len(search) > 0:
        print(search)
        units = units.filter(
            Q(name__icontains=search) |
            Q(model_name__icontains=search) |
            Q(services__name__icontains=search) |
            Q(category__name__icontains=search)
        ).distinct()
        print(type(units))

    if name is not None:
        units = units.filter(name=name)

    if sort_price is not None and len(sort_price) > 0:
        if sort_price == 'inc':
            units = units.order_by('minimal_price_UAH')
        if sort_price == 'dec':
            units = units.order_by('-minimal_price_UAH')

    if category is not None and len(category) > 0:
        units = units.filter(category_id__in=category.split(',')).distinct()

    if model_name is not None and len(model_name) > 0:
        units = units.filter(model_name__in=model_name.split(',')).distinct()

    if manufacturers is not None and len(manufacturers) > 0:
        units = units.filter(manufacturers__name__in=manufacturers.split(',')).distinct()

    if services is not None and len(services) > 0:
        units = units.filter(services__in=services.split(',')).distinct()

    return await units

