from collections import deque

from compmath_calc_server.models.ni.dto import TableRow
from compmath_calc_server.utils.func import make_callable
from compmath_calc_server.exceptions import BadRequest
from compmath_calc_server.models import GraphicBuilder
from compmath_calc_server.models.ni.dto import InputNIModel, OutputNIModel


def calc(data: InputNIModel) -> OutputNIModel:
    function = make_callable(data.fx)
    a = data.a
    b = data.b
    n = data.intervals
    x_limits = data.x_limits
    y_limits = data.y_limits

    if a > b:
        raise BadRequest("Левая граница интервала не может быть больше правой")

    graphic = GraphicBuilder(x_limits=x_limits, y_limits=y_limits)
    graphic.add_graph(function)
    graphic.add_graph(lambda x: 0, width=2)
    graphic.add_graph(fy=lambda y: a, width=2, y_limits=(function(a), 0))
    graphic.add_graph(fy=lambda y: b, width=2, y_limits=(function(b), 0))

    rows = deque(maxlen=1000)

    h = (b - a) / n
    result = 0
    for i in range(n):
        x = a + i * h
        y = function(x + h)
        s = y * h
        result += s

        if n <= 100:
            graphic.add_rect(x, y, x + h, 0, color="red")

        if n <= 1000 or i == 0 or i == n - 1:
            rows.append(TableRow(num=i, x=x, y=y, value=s))

    graphic.add_graph(
        function,
        x_limits=(a, b),
        width=2,
        fill="red" if n > 100 else None
    )

    return OutputNIModel(
        graphic_items=graphic.build(),
        table=list(rows),
        result=result
    )


