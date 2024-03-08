from compmath_calc_server.models.ni.dto import OutputNIModel, OutputNInterModel
from compmath_calc_server.views import BaseView


class NIResponse(BaseView):
    content: OutputNIModel


class NInterResponse(BaseView):
    content: OutputNInterModel
