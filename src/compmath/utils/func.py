from typing import Callable, Protocol
from sympy import sympify, lambdify, symbols, SympifyError, Basic, solve
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
    symbols_list = [s for s in expr.free_symbols if isinstance(s, Symbol)]
    symbols_dict = {str(s): s for s in symbols_list}

    lambda_func = lambdify(symbols_list, expr, 'numpy')

    def wrapped_func(a0: float | int | None = None, a1: float | int | None = None):
        if 'x' in symbols_dict and 'y' in symbols_dict:
            return lambda_func(a0, a1)
        elif 'x' in symbols_dict:
            return lambda_func(a0 or a1)
        elif 'y' in symbols_dict:
            return lambda_func(a1 or a0)
        else:
            return lambda_func()

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
