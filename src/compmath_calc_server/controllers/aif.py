from fastapi import APIRouter

from compmath_calc_server.models.aif.dto import InputAIFModel, InputInterpModel
from compmath_calc_server.models.aif import alsm, interspline
from compmath_calc_server.views import AIFResponse, InterpResponse

router = APIRouter()


@router.post("/alsm/calculate", response_model=AIFResponse, status_code=200)
def calculate_alsm(data: InputAIFModel):
    return AIFResponse(content=alsm.calc(data))


@router.post("/interp/calculate", response_model=InterpResponse, status_code=200)
def calculate_interp(data: InputInterpModel):
    return InterpResponse(content=interspline.calc(data))
