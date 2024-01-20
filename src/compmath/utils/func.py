from typing import Callable


class FunctionValidateError(Exception):
    ...


def make_callable(fx: str) -> Callable[[float | int], float]:
    """
    Создание функции из строки

    :param fx: Строка с функцией
    :return: Функция
    """
    try:
        return lambda x: eval(
            fx,
            {
                "x": x

            }
        )
    except Exception as error:
        raise FunctionValidateError(error)


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
