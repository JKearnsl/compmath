from typing import cast

import numpy as np

from compmath_calc_server.exceptions import BadRequest
from compmath_calc_server.utils.func import make_callable, solve_rel_var, is_converges, evenly_spaced_elements
from compmath_calc_server.models import GraphicBuilder
from compmath_calc_server.models.sne.dto import InputSNEModel, OutputSNEModel, TableRow


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

    x_vector = np.array([0, 0], dtype=float)

    k = 0
    delta = 2 * eps
    while delta > eps and k < iters_limit:
        k += 1

        x0 = x_vector.copy()

        for i in range(len(x_vector)):
            x_vector[i] = fi_x_y[i](*x0)

        delta = np.max(np.abs(x_vector - x0))

        table.append(TableRow(iter_num=k,vector=list(x_vector), delta=delta))
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
