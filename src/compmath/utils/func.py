from typing import Callable, Protocol

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

    try:
        lambda_func = lambdify(symbols_list, expr, 'numpy')
    except TypeError:
        raise FunctionValidateError(f"Invalid literal: {func}")

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
