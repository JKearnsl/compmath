from copy import deepcopy
from typing import Callable, Protocol, Sequence

import numpy as np
from sympy import sympify, lambdify, SympifyError, Basic, solve
from sympy.core import Symbol


class FunctionValidateError(Exception):
    ...


class ConstProtocol(Protocol):
    def __call__(self) -> float:
        ...


class OneArgProtocol(Protocol):
    def __call__(self, x: float | int) -> float:
        ...


class FuncReturn(Protocol):
    def __call__(self, x: float | int | None = None, y: float | int | None = None) -> float:
        ...


def is_valid_func(func: str, valid_symbols: list[str] = None) -> bool:
    if valid_symbols is None:
        valid_symbols = ["x", "y"]
    try:
        expr = sympify(func)
        symbols_list = [str(s) for s in expr.free_symbols]
        if all(s in valid_symbols for s in symbols_list):
            return True
        return False
    except (SympifyError, TypeError):
        return False


def make_callable(func: str | Basic) -> FuncReturn:
    """
    Создание функции из строки

    :param func: Строка с функцией
    :return: Функция
    """
    if isinstance(func, str):
        try:
            expr = sympify(func)
        except (SympifyError, TypeError):
            raise FunctionValidateError(f"Invalid literal: {func}")
    else:
        expr = func

    # Список символов из выражения
    try:
        symbols_str_list = [str(s) for s in expr.free_symbols if isinstance(s, Symbol)]
    except AttributeError:
        raise FunctionValidateError(f"Invalid literal: {func}")

    if len(symbols_str_list) > 1 and "x" in symbols_str_list:
        symbols_str_list.sort(key=lambda var: var != "x")

    symbols_list = [Symbol(s) for s in symbols_str_list]

    lambda_func = lambdify(symbols_list, expr, 'numpy')

    def wrapped_func(a0: float | int | None = None, a1: float | int | None = None):
        if 'x' in symbols_str_list and 'y' in symbols_str_list:
            return lambda_func(a0, a1)
        elif 'x' in symbols_str_list:
            return lambda_func(a0 if a0 is not None else a1)
        elif 'y' in symbols_str_list:
            return lambda_func(a1 if a1 is not None else a0)
        else:
            return lambda_func()

    return wrapped_func


def solve_rel_var(func: str | Basic, var: str):
    """
    Решение уравнения относительно переменной

    :param func: Уравнение
    :param var: Переменная
    :return: Функция
    """
    if isinstance(func, str):
        try:
            expr = sympify(func)
        except (SympifyError, TypeError):
            raise FunctionValidateError(f"Invalid literal: {func}")
    elif isinstance(func, Basic):
        expr = func
    else:
        raise ValueError(f"Invalid literal: {func}")

    return solve(expr, var)


def derivative(fx: Callable[[float | int], float], h: float = 0.0001) -> Callable[[float | int], float]:
    """
    Вычисление производной функции

    :param fx:
    :param h: приращение аргумента
    :return: производная функции fx
    """

    return lambda x: (fx(x + h) - fx(x)) / h


def tangent(fx: Callable[[float | int], float], x0: float | int) -> Callable[[float | int], float]:
    """
    Уравнение касательной

    y = f(x0) + f'(x0)(x-x0)


    :param fx: функция графика
    :param x0: точка касания
    :return: уравнение касательной
    """

    return lambda x: fx(x0) + derivative(fx)(x0) * (x - x0)


def line_between_points(
        x1: float | int,
        y1: float | int,
        x2: float | int,
        y2: float | int
) -> Callable[[float | int], float]:
    """
     Уравнение прямой в форме y = mx + b

    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return lambda x: m * x + b


def gauss_calc(
        a_matrix: Sequence[Sequence[float]],
        b_vector: Sequence[float],
        n: int
) -> tuple[Sequence[float], Sequence[float], Sequence[Sequence[float]]] | None:
    """
    Метод Гаусса


    :param a_matrix:
    :param b_vector:
    :param n:
    :return: Вектор решений, вектор невязок, преобразованная матрица
    """
    a_matrix = deepcopy(a_matrix)
    b_vector = deepcopy(b_vector)

    a_matrix_copy = deepcopy(a_matrix)
    b_vector_copy = deepcopy(b_vector)

    for k in range(n - 1):
        if a_matrix[k][k] == 0:
            m = k + 1
            while m < n and a_matrix[m][k] == 0:
                m += 1
            if m == n:
                return None  # Система не обусловлена, не удалось заменить строку
            else:
                # Обмен строк
                a_matrix[k], a_matrix[m] = a_matrix[m], a_matrix[k]
                b_vector[k], b_vector[m] = b_vector[m], b_vector[k]

        # Прямой ход
        for i in range(k + 1, n):
            q = a_matrix[i][k] / a_matrix[k][k]
            for j in range(k, n):
                a_matrix[i][j] -= q * a_matrix[k][j]
            b_vector[i] -= q * b_vector[k]

    x_vector = [b_vector[c] / a_matrix[c][c] for c in range(n)]

    # Обратный ход
    for i in range(n - 1, -1, -1):
        s = sum(a_matrix[i][j] * x_vector[j] for j in range(i + 1, n))
        x_vector[i] = (b_vector[i] - s) / a_matrix[i][i]

    # Невязки
    delta_vector = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += a_matrix_copy[i][j] * x_vector[j]
        delta_vector.append(b_vector_copy[i] - s)

    result_matrix = []
    for i in range(n):
        result_matrix.append([a_matrix_copy[i][j] for j in range(n)])
        result_matrix[i].append(b_vector_copy[i])

    return x_vector, delta_vector, result_matrix


def is_diagonal_dominance(matrix: Sequence[Sequence[float]]) -> bool:
    matrix = np.array(matrix)

    diagonal = np.abs(matrix.diagonal())

    # Сумма абсолютных значений элементов вне диагонали
    off_diagonal = np.sum(np.abs(matrix), axis=1) - diagonal

    # Проверить диагональное преобладание
    return np.all(diagonal >= off_diagonal)
