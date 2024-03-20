from typing import cast

import numpy as np
from sympy import diff

from compmath_calc_server.utils.func import make_callable, solve_rel_var
from compmath_calc_server.exceptions import BadRequest
from compmath_calc_server.models import GraphicBuilder
from compmath_calc_server.models.sne.dto import InputSNEModel, OutputSNEModel, TableRow
from compmath_calc_server.utils.func import is_converges, evenly_spaced_elements


def calc(data: InputSNEModel) -> OutputSNEModel:
    table = []
    solve_log = []
    graphics = []

    if len(data.equations) != 2:
        raise BadRequest("Поддерживается только решение системы из двух уравнений")

    func_str_1 = data.equations[0]
    func_str_2 = data.equations[1]
    eps = data.eps
    initial_guess = data.initial_guess
    iters_limit = data.iters_limit
    x_limits = data.x_limits
    y_limits = data.y_limits

    solve_log.append(f"Уравнение 1: {func_str_1}")
    solve_log.append(f"Уравнение 2: {func_str_2}")

    # Проверка итерационной сходимости
    converged, log = is_converges(func_str_1, func_str_2, initial_guess, True)
    solve_log.extend(log)

    if not converged:
        raise BadRequest("Не выполнено условие сходимости")

    # Решение

    fi_x_y = (
        make_callable(solve_rel_var(func_str_1, "x")[0]),
        make_callable(solve_rel_var(func_str_2, "y")[0])
    )

    # Матрица Якоби
    w = [
        [diff(func_str_1, "x"), diff(func_str_1, "y")],
        [diff(func_str_2, "x"), diff(func_str_2, "y")]
    ]
    x_vector = np.array([0, 0], dtype=float)

    solve_log.append(f"Матрица Якоби:")
    solve_log.append(f"W(x, y) = \n{'\n'.join('\t'.join(str(el) for el in row) for row in w)}")

    for i, row in enumerate(w):
        for j, el in enumerate(row):
            w[i][j] = make_callable(el)

    k = 0
    delta = 2 * eps
    while delta > eps and k < iters_limit:
        k += 1

        # Вектор поправок delta_x_vector = - W(x_vector_1, x_vector_2)^-1 * F(x_vector_1, x_vector_2)
        w_matrix = np.array([
            [w[0][0](*x_vector), w[0][1](*x_vector)],
            [w[1][0](*x_vector), w[1][1](*x_vector)]
        ])

        delta_x = -np.linalg.inv(w_matrix) @ np.array([
            make_callable(func_str_1)(*x_vector),
            make_callable(func_str_2)(*x_vector)
        ])

        # Уточнение решения
        x_vector = delta_x + x_vector

        # Расчет оценки достаточной точности
        delta = np.mean(np.abs(delta_x))

        table.append(TableRow(iter_num=k, vector=x_vector, delta=delta))
        graphic = GraphicBuilder(x_limits=x_limits, y_limits=y_limits)
        graphic.add_graph(fx=fi_x_y[0], color="blue")
        graphic.add_graph(fy=fi_x_y[1], color="red")
        graphic.add_point(
            cast(float, x_vector[1]),
            cast(float, x_vector[0]),
            color="green"
        )
        graphics.append(graphic.build())

    solve_log.append(f"\nРешение: {x_vector}")

    return OutputSNEModel(
        solve_log=solve_log,
        table=table,
        graphics=evenly_spaced_elements(graphics, 10)
    )
