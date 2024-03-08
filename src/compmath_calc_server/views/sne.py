from compmath_calc_server.models.sne.dto import OutputSNEModel
from compmath_calc_server.views import BaseView


class SNEResponse(BaseView):
    content: OutputSNEModel
