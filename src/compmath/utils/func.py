from typing import Callable, Protocol
from sympy import sympify, lambdify, symbols, SympifyError, Basic
from sympy.core import Symbol


class FunctionValidateError(Exception):
    ...


class ConstProtocol(Protocol):
    def __call__(self) -> float:
        ...


class OneArgProtocol(Protocol):
    def __call__(self, x: float | int) -> float:
        ...


class FuncProtocol(Protocol):
    def __call__(self, x: float | int | None = None, y: float | int | None = None) -> float:
        ...


def make_callable(fx: str | Basic) -> FuncProtocol:
    """
    Создание функции из строки

    :param fx: Строка с функцией
    :return: Функция
    """
    if isinstance(fx, str):
        try:
            expr = sympify(fx)
        except (SympifyError, TypeError):
            raise FunctionValidateError(f"Invalid literal: {fx}")
    else:
        expr = fx

    # Список символов из выражения
    symbols_list = [s for s in expr.free_symbols if isinstance(s, Symbol)]

    # Если переменных нет, константа
    if not symbols_list:
        def constant_func(*args):
            return expr

        return constant_func

    sym_symbols = [symbols(str(symbol)) for symbol in symbols_list]
    symbols_dict = {str(s): s for s in sym_symbols}

    func = lambdify(sym_symbols, expr, 'numpy')

    def wrapped_func(x=None, y=None):
        if 'x' in symbols_dict and 'y' in symbols_dict:
            return func(x, y)
        elif 'x' in symbols_dict or 'y' in symbols_dict:
            return func(x)
        elif 'y' in symbols_dict:
            return func(y)
        else:
            raise ValueError("No variables found in the expression")

    return wrapped_func


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
