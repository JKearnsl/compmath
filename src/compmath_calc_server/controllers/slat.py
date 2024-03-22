from fastapi import APIRouter

from compmath_calc_server.models.slat.dto import InputSLATModel
from compmath_calc_server.models.slat import (
    sim,
    zm,
    gm
)
from compmath_calc_server.views import SLATResponse

router = APIRouter()


@router.post("/sim/calculate", response_model=SLATResponse, status_code=200)
def calculate_sim(data: InputSLATModel):
    return SLATResponse(content=sim.calc(data))


@router.post("/zm/calculate", response_model=SLATResponse, status_code=200)
def calculate_zm(data: InputSLATModel):
    return SLATResponse(content=zm.calc(data))


@router.post("/gm/calculate", response_model=SLATResponse, status_code=200)
def calculate_gm(data: InputSLATModel):
    return SLATResponse(content=gm.calc(data))
