import numpy as np
from sympy import integrate, sympify, pi

from compmath.utils.func import make_callable
from compmath_calc_server.utils.func import arc_length
from compmath_calc_server.exceptions import BadRequest
from compmath_calc_server.models import GraphicBuilder
from compmath_calc_server.models.ni.dto import InputNInterModel, OutputNInterModel
from compmath_calc_server.utils.func import surface_area


def calc(data: InputNInterModel) -> OutputNInterModel:
    fx_str = data.fx
    a = data.a
    b = data.b

    fx = sympify(fx_str)

    if a > b:
        raise BadRequest("Левая граница интервала не может быть больше правой")

    reference_result = integrate(fx, ('x', a, b)).evalf()
    surface_area_value = surface_area(fx_str, a, b, 'x')
    volume = (pi * integrate(fx ** 2, ('x', a, b))).evalf()
    arc_length_value = arc_length(fx_str, a, b, 'x')

    # Границы по переменной v
    v0 = 0
    v1 = 2 * np.pi

    # Количество точек на поверхности
    m = 100

    # Функция
    func = make_callable(fx_str)

    # Создание поверхности вращения
    verts = []
    for u in np.linspace(a, b, m):
        for v in np.linspace(v0, v1, m):
            verts.append([u, func(u) * np.sin(v), func(u) * np.cos(v)])

    # Создание граней для поверхности
    faces = []
    for i in range(m - 1):
        for j in range(m - 1):
            faces.append([i * m + j, i * m + j + 1, (i + 1) * m + j + 1, (i + 1) * m + j])

    graphic = GraphicBuilder()
    graphic.add_mesh(
        vertexes=verts,
        faces=faces,
        shader="normalColor"
    )

    return OutputNInterModel(
        graphic_items=graphic.build(),
        reference_result=reference_result,
        surface_area=surface_area_value,
        volume=volume,
        arc_length=arc_length_value
    )
