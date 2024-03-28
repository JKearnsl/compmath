from copy import deepcopy
from typing import Sequence

import numpy as np


def normalize_matrix(a_matrix: list[list[float]], b_vector: list[float]) -> tuple[np.ndarray[float], np.ndarray[float]]:
    new_matrix = np.array(deepcopy(a_matrix), dtype=float)
    a_matrix = np.dot(new_matrix.T, new_matrix)
    b_matrix = np.dot(new_matrix.T, b_vector)
    return a_matrix, b_matrix


def is_diagonal_dominance(matrix: Sequence[Sequence[float]]) -> bool:
    matrix = np.array(matrix)

    diagonal = np.abs(matrix.diagonal())

    # Сумма абсолютных значений элементов вне диагонали
    off_diagonal = np.sum(np.abs(matrix), axis=1) - diagonal

    # Проверить диагональное преобладание
    return np.all(diagonal > off_diagonal)
