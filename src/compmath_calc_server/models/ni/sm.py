from compmath_calc_server.utils.func import make_callable
from compmath_calc_server.exceptions import BadRequest
from compmath_calc_server.models import GraphicBuilder
from compmath_calc_server.models.ni.dto import OutputNIModel, InputNIModel


def calc(data: InputNIModel) -> OutputNIModel:
    function = make_callable(data.fx)
    a = data.a
    b = data.b
    n = data.intervals
    x_limits = data.x_limits
    y_limits = data.y_limits

    if a > b:
        raise BadRequest("Левая граница интервала не может быть больше правой")

    if n % 2 != 0:
        raise BadRequest("Количество интервалов должно быть четным")

    graphic = GraphicBuilder(x_limits=x_limits, y_limits=y_limits)
    graphic.add_graph(function)
    graphic.add_graph(lambda x: 0, width=2, x_limits=(a, b))
    graphic.add_graph(fy=lambda y: a, width=2, y_limits=(function(a), 0))
    graphic.add_graph(fy=lambda y: b, width=2, y_limits=(function(b), 0))

    h = (b - a) / (2 * n)
    sum1 = 0
    sum2 = 0
    for i in range(2 * n):
        if i % 2 != 0:
            sum1 += function(a + i * h)
        elif i != 0:
            sum2 += function(a + i * h)

    result = h / 3 * (function(a) + 4 * sum1 + 2 * sum2 + function(b))

    return OutputNIModel(
        graphic_items=graphic.build(),
        result=result,
        table=[]
    )
