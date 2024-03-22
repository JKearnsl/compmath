from math import sqrt
from typing import Sequence

from compmath_calc_server.models.slat.dto import InputSLATModel, TableRow
from compmath_calc_server.models.slat.utils import is_diagonal_dominance, transform_matrix, normalize_matrix


def calc(data: InputSLATModel) -> list[tuple[list[str], list[TableRow], str]]:
    results = []

    a_matrix = data.a_matrix
    b_vector = data.b_vector
    eps = data.eps
    iters_limit = data.iters_limit
    x0 = data.x0
    if x0 is None:
        x0 = [0] * len(a_matrix)

    results.append(calc_original(a_matrix, b_vector, x0, eps, iters_limit))
    results.append(calc_transformed(a_matrix, b_vector, x0, eps, iters_limit))
    results.append(calc_normalized(a_matrix, b_vector, x0, eps, iters_limit))

    return results


def calc_sim(
        a_matrix: Sequence[Sequence[float]],
        b_vector: Sequence[float],
        x0: list[float],
        eps: float,
        iters_limit: int
) -> tuple[list[float], list[TableRow]]:
    k = 0
    n = len(a_matrix)
    x = x0.copy()

    table = []

    while True:
        k += 1
        x_prev = x.copy()
        for i in range(n):
            s = sum(a_matrix[i][j] * x_prev[j] for j in range(n) if j != i)
            x[i] = (b_vector[i] - s) / a_matrix[i][i]

        # Оценка точности
        delta = sqrt(max((x[i] - x_prev[i]) ** 2 for i in range(n)))

        table.append(
            TableRow(
                iter_num=k,
                vector=x.copy(),
                delta=delta
            )
        )

        if delta <= eps or k >= iters_limit:
            break

    return x, table


def calc_original(
        a_matrix: list[list[float]],
        b_vector: list[float],
        x0: list[float],
        eps: float,
        iters_limit: int
) -> tuple[list[str], list[TableRow], str]:
    # Исходная матрица
    log = ["\nИсходная матрица\n"]
    for i, row in enumerate(a_matrix):
        log.append(
            "\t".join(str(cell) for cell in row) + "\t|   " + str(b_vector[i])
        )

    log.append("\nРешение МПИ\n")
    result = calc_sim(a_matrix, b_vector, x0, eps, iters_limit)
    log.append("\n".join(str(cell) for cell in result[0]))

    log.append("\nКол-во итераций\n")
    log.append(str(len(result[1])))

    return log, result[1], "Исходная матрица"


def calc_transformed(
        a_matrix: list[list[float]],
        b_vector: list[float],
        x0: list[float],
        eps: float,
        iters_limit: int
) -> tuple[list[str], list[TableRow], str]:
    # Преобразованная матрица
    log = ["\nИсходная матрица\n"]
    for i, row in enumerate(a_matrix):
        log.append(
            "\t".join(str(cell) for cell in row) + "\t|   " + str(b_vector[i])
        )
    log.append("")

    for i, row in enumerate(a_matrix):
        sum_row = sum(abs(cell) for j, cell in enumerate(row) if j != i)
        log.append(
            f"sum({', '.join(f'|{cell}|' for j, cell in enumerate(row) if j != i)}) = "
            f"{sum_row}   {'>' if sum_row > abs(row[i]) else '<='}   |{row[i]}|"
            f"\t[{'-' if sum_row > abs(row[i]) else '+'}]"
        )
    log.append("")

    if is_diagonal_dominance(a_matrix):
        log.append("Матрица обладает диагональным преобладанием")
        log.append("Необходимости в элементарных преобразованиях исходной матрицы нет")
    else:
        log.append("Матрица не обладает диагональным преобладанием")
        log.append("Необходимо преобразовать исходную матрицу")

        log.append("\nПреобразованная матрица\n")
        transformed_a_matrix, transformed_b_vector, transform_log = transform_matrix(a_matrix, b_vector)
        log.append("Шаги:")
        log.extend(transform_log)
        log.append("")

    log.append("\nРешение МПИ\n")
    result = calc_sim(a_matrix, b_vector, x0, eps, iters_limit)
    log.append("\n".join(str(cell) for cell in result[0]))

    log.append("\nКол-во итераций\n")
    log.append(str(len(result[1])))

    return log, result[1], "Преобразованная матрица"


def calc_normalized(
        a_matrix: list[list[float]],
        b_vector: list[float],
        x0: list[float],
        eps: float,
        iters_limit: int
) -> tuple[list[str], list[TableRow], str]:
    # Нормализованная матрица
    log = ["\nИсходная матрица\n"]
    for i, row in enumerate(a_matrix):
        log.append(
            "\t".join(str(cell) for cell in row) + "\t|   " + str(b_vector[i])
        )

    log.append("\nНормализованная матрица\n")
    a_matrix, b_vector = normalize_matrix(a_matrix, b_vector)
    for i, row in enumerate(a_matrix):
        log.append(
            "\t".join(str(round(cell, 2)) for cell in row) + "\t|   " + str(round(b_vector[i], 2))
        )

    log.append("\nРешение МПИ\n")
    result = calc_sim(a_matrix, b_vector, x0, eps, iters_limit)
    log.append("\n".join(str(cell) for cell in result[0]))

    log.append("\nКол-во итераций\n")
    log.append(str(len(result[1])))

    return log, result[1], "Нормализованная матрица"
