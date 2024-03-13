from sympy import integrate, sympify

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

    graphic = GraphicBuilder(x_limits=x_limits, y_limits=y_limits)
    graphic.add_graph(function)
    graphic.add_graph(lambda x: 0, width=2, x_limits=(a, b))
    graphic.add_graph(fy=lambda y: a, width=2, y_limits=(function(a), 0))
    graphic.add_graph(fy=lambda y: b, width=2, y_limits=(function(b), 0))

    h = (b - a) / n
    s = (function(b) - function(a)) / 2
    for i in range(n):
        s += function(a + h * i) + 2 * function(a + i * h + h / 2)
    result = s * (h / 3)

    reference_result = integrate(sympify(data.fx), ('x', a, b)).evalf()
    abs_delta = abs(reference_result - result)
    relative_delta = abs(abs_delta / reference_result) * 100

    return OutputNIModel(
        graphic_items=graphic.build(),
        table=[],
        result=result,
        abs_delta=abs_delta,
        relative_delta=relative_delta
    )
