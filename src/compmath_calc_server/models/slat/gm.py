from compmath_calc_server.models.slat.utils import (
    normalize_matrix,
    transform_matrix,
    is_diagonal_dominance
)
from compmath_calc_server.models.slat.dto import InputSLATModel, TableRow
from compmath_calc_server.utils.func import gauss_calc


def calc(data: InputSLATModel) -> list[tuple[list[str], list[TableRow], str]]:
    results = []

    a_matrix = data.a_matrix
    b_vector = data.b_vector

    results.append(calc_original(a_matrix, b_vector))
    results.append(calc_transform(a_matrix, b_vector))
    results.append(calc_normalized(a_matrix, b_vector))

    return results


def calc_original(a_matrix: list[list[float]], b_vector: list[float]) -> tuple[list[str], list[TableRow], str]:
    # Исходная матрица
    n = len(a_matrix)
    log = ["\nИсходная матрица\n"]
    for i, row in enumerate(a_matrix):
        log.append(
            "\t".join(str(cell) for cell in row) + "\t|   " + str(b_vector[i])
        )

    log.append("\nПрямой ход метода Гаусса\n")
    original_gauss_vector = gauss_calc(a_matrix, b_vector, n)
    if original_gauss_vector is None:
        log.append("Система не обусловлена")
        return log, [], "Исходная матрица"

    log.append("\n".join(str(cell) for cell in original_gauss_vector[0]))

    log.append("\nВектор невязок\n")
    log.append("\n".join(str(cell) for cell in original_gauss_vector[1]))

    log.append("\nТреугольная матрица\n")
    for row in original_gauss_vector[2]:
        log.append("\t".join(str(round(cell, 2)) for cell in row))

    return log, [], "Исходная матрица"


def calc_transform(a_matrix: list[list[float]], b_vector: list[float]) -> tuple[list[str], list[TableRow], str]:
    # Преобразованная матрица
    n = len(a_matrix)
    log = ["\nИсходная матрица\n"]
    for i, row in enumerate(a_matrix):
        log.append(
            "\t".join(str(cell) for cell in row) + "\t|   " + str(b_vector[i])
        )
    log.append("")

    for i, row in enumerate(a_matrix):
        sum_row = sum(abs(cell) for j, cell in enumerate(row) if j != i)
        log.append(
            f"sum({", ".join(f'|{cell}|' for j, cell in enumerate(row) if j != i)}) = "
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
        for i, row in enumerate(transformed_a_matrix):
            log.append(
                "\t".join(str(round(cell, 2)) for cell in row) + "\t|   " + str(round(transformed_b_vector[i], 2))
            )

        log.append("\nРешение методом Гаусса\n")

        transformed_gauss_vector = gauss_calc(transformed_a_matrix, transformed_b_vector, n)
        if transformed_gauss_vector is None:
            log.append("Система не обусловлена")
            return log, [], "Преобразованная матрица"

        log.append("\n".join(str(cell) for cell in transformed_gauss_vector[0]))

        log.append("\nВектор невязок\n")
        log.append("\n".join(str(round(cell, 2)) for cell in transformed_gauss_vector[1]))

        log.append("\nТреугольная матрица\n")
        for row in transformed_gauss_vector[2]:
            log.append("\t".join(str(round(cell, 2)) for cell in row))

    return log, [], "Преобразованная матрица"


def calc_normalized(a_matrix: list[list[float]], b_vector: list[float]) -> tuple[list[str], list[TableRow], str]:
    # Нормализованная матрица
    n = len(a_matrix)
    log = ["\nНормализованная матрица\n"]
    normal_a_matrix, normal_b_vector = normalize_matrix(a_matrix, b_vector)
    for i, row in enumerate(normal_a_matrix):
        log.append(
            "\t".join(str(round(cell, 2)) for cell in row) + "\t|   " + str(round(normal_b_vector[i], 2))
        )

    log.append("\nРешение методом Гаусса\n")
    gauss_vector = gauss_calc(normal_a_matrix, normal_b_vector, n)
    if gauss_vector is None:
        log.append("Система не обусловлена")
        return log, [], "Нормализованная матрица"

    log.append("\n".join(str(cell) for cell in gauss_vector[0]))

    log.append("\nВектор невязок\n")
    log.append("\n".join(str(round(cell, 2)) for cell in gauss_vector[1]))

    log.append("\nТреугольная матрица\n")
    for row in gauss_vector[2]:
        log.append("\t".join(str(round(cell, 2)) for cell in row))

    return log, [], "Нормализованная матрица"
