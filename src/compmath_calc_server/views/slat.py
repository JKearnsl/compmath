from compmath_calc_server.models.slat.dto import TableRow
from compmath_calc_server.views import BaseView


class SLATResponse(BaseView):
    content: list[tuple[list[str], list[TableRow], str]]
