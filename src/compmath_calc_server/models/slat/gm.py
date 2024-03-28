from compmath_calc_server.models.slat.dto import InputSLATModel, TableRow
from compmath_calc_server.utils.func import gauss_calc


def calc(data: InputSLATModel) -> list[tuple[list[str], list[TableRow], str]]:
    results = []

    a_matrix = data.a_matrix
    b_vector = data.b_vector

    results.append(calc_original(a_matrix, b_vector))

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
