from sympy import integrate, sympify, pi

from compmath_calc_server.utils.func import arc_length
from compmath_calc_server.exceptions import BadRequest
from compmath_calc_server.models import GraphicBuilder
from compmath_calc_server.models.ni.dto import InputNInterModel, OutputNInterModel
from compmath_calc_server.utils.func import surface_area


def calc(data: InputNInterModel) -> OutputNInterModel:
    fx_str = data.fx
    a = data.a
    b = data.b
    x_limits = data.x_limits
    y_limits = data.y_limits

    fx = sympify(fx_str)

    if a > b:
        raise BadRequest("Левая граница интервала не может быть больше правой")

    reference_result = integrate(fx, ('x', a, b)).evalf()
    surface_area_value = surface_area(fx_str, a, b, 'x')
    volume = (pi * integrate(fx ** 2, ('x', a, b))).evalf()
    arc_length_value = arc_length(fx_str, a, b, 'x')

    # graphic = GraphicBuilder(x_limits, y_limits)
    # graphic.add_surface(fx, (a, b))

    return OutputNInterModel(
        graphic_items=[],
        reference_result=reference_result,
        surface_area=surface_area_value,
        volume=volume,
        arc_length=arc_length_value
    )
