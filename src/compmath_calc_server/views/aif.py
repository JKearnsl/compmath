from compmath_calc_server.models.aif.dto import ResultAIFItem, ResultInterpItem
from compmath_calc_server.views import BaseView


class AIFResponse(BaseView):
    content: list[ResultAIFItem]


class InterpResponse(BaseView):
    content: list[ResultInterpItem]
