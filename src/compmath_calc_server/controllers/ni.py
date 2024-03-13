from fastapi import APIRouter

from compmath_calc_server.models.ni.dto import InputNIModel, InputNInterModel
from compmath_calc_server.models.ni import (
    lrm,
    mrm,
    rrm,
    sm2,
    sm1,
    tm,
    intermediate
)
from compmath_calc_server.views import NIResponse, NInterResponse

router = APIRouter()


@router.post("/lrm/calculate", response_model=NIResponse, status_code=200)
def calculate_lrm(data: InputNIModel):
    return NIResponse(content=lrm.calc(data))


@router.post("/mrm/calculate", response_model=NIResponse, status_code=200)
def calculate_mrm(data: InputNIModel):
    return NIResponse(content=mrm.calc(data))


@router.post("/rrm/calculate", response_model=NIResponse, status_code=200)
def calculate_rrm(data: InputNIModel):
    return NIResponse(content=rrm.calc(data))


@router.post("/sm2/calculate", response_model=NIResponse, status_code=200)
def calculate_sm2(data: InputNIModel):
    return NIResponse(content=sm2.calc(data))


@router.post("/sm1/calculate", response_model=NIResponse, status_code=200)
def calculate_sm1(data: InputNIModel):
    return NIResponse(content=sm1.calc(data))


@router.post("/tm/calculate", response_model=NIResponse, status_code=200)
def calculate_tm(data: InputNIModel):
    return NIResponse(content=tm.calc(data))


@router.post("/intermediate/calculate", response_model=NInterResponse, status_code=200)
def calculate_intermediate(data: InputNInterModel):
    return NInterResponse(content=intermediate.calc(data))
