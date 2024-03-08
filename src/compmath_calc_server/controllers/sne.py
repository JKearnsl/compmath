from fastapi import APIRouter

from compmath_calc_server.models.sne.dto import InputSNEModel
from compmath_calc_server.models.sne import sim, ntm, zm
from compmath_calc_server.views import SNEResponse

router = APIRouter()


@router.post("/sim/calculate", response_model=SNEResponse, status_code=200)
def calculate_sim(data: InputSNEModel):
    return SNEResponse(content=sim.calc(data))


@router.post("/ntm/calculate", response_model=SNEResponse, status_code=200)
def calculate_ntm(data: InputSNEModel):
    return SNEResponse(content=ntm.calc(data))


@router.post("/zm/calculate", response_model=SNEResponse, status_code=200)
def calculate_zm(data: InputSNEModel):
    return SNEResponse(content=zm.calc(data))
