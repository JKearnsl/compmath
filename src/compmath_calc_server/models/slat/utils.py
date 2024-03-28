from copy import deepcopy
from typing import Sequence

import numpy as np
import sympy as sp


def normalize_matrix(a_matrix: list[list[float]], b_vector: list[float]) -> tuple[np.ndarray[float], np.ndarray[float]]:
    new_matrix = np.array(deepcopy(a_matrix), dtype=float)
    a_matrix = np.dot(new_matrix.T, new_matrix)
    b_matrix = np.dot(new_matrix.T, b_vector)
    return a_matrix, b_matrix


def transform_matrix(
        matrix: Sequence[Sequence[float]],
        vector: Sequence[float]
) -> tuple[Sequence[Sequence[float]], Sequence[float], list[str]]:
    a_matrix = deepcopy(matrix)
    b_vector = deepcopy(vector)
    n = len(a_matrix)

    # Создание символьных матриц для работы с элементарными преобразованиями
    a_sym = sp.Matrix(a_matrix)
    b_sym = sp.Matrix(b_vector)
    transformations_log = []  # Лог для записи действий

    for i in range(n):
        # Поиск максимального элемента в столбце i
        max_index = i
        for j in range(i + 1, n):
            if abs(a_sym[j, i]) > abs(a_sym[max_index, i]):
                max_index = j
        if max_index != i:
            # Перестановка строк для диагонального преобладания
            a_sym.row_swap(i, max_index)
            b_sym.row_swap(i, max_index)
            transformations_log.append(f"Перестановка строк: {i + 1} и {max_index + 1}")

        # Выполнение диагонального преобразования
        pivot = a_sym[i, i]
        for j in range(i + 1, n):
            if pivot == 0:
                break  # Пропустить, если главный элемент равен нулю
            ratio = a_sym[j, i] / pivot
            a_sym.row_op(j, lambda x, k: x - ratio * a_sym[i, k])
            b_sym.row_op(j, lambda x, k: x - ratio * b_sym[i, k])
            transformations_log.append(f"Вычитание из строки {j + 1} строки {i + 1}, умноженной на {ratio}")

    # Возвращение результатов преобразований и лога
    return a_sym.tolist(), [el[0] for el in b_sym.tolist()], transformations_log


def is_diagonal_dominance(matrix: Sequence[Sequence[float]]) -> bool:
    matrix = np.array(matrix)

    diagonal = np.abs(matrix.diagonal())

    # Сумма абсолютных значений элементов вне диагонали
    off_diagonal = np.sum(np.abs(matrix), axis=1) - diagonal

    # Проверить диагональное преобладание
    return np.all(diagonal > off_diagonal)
