from typing import Callable, Protocol, Sequence

import numpy as np
from sympy import sympify, lambdify, SympifyError, Basic, solve, symbols
from sympy.core import Symbol
from numpy.linalg import lstsq
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline


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
    symbols_str_list = [str(s) for s in expr.free_symbols if isinstance(s, Symbol)]

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


def linfit(x: list[float], y: list[float], func: Callable[[float], tuple]) -> tuple:
    """
    Возвращает вектор коэффициентов линейной комбинации функций в векторе func,
    наилучшим образом аппроксимирующей данные в векторах x и y.

    :param x: вектор аргументов
    :param y: вектор значений
    :param func: функция, принимающая один аргумент и возвращающая кортеж значений
    :return: кортеж коэффициентов аппроксимации
    """
    # Создание символов для переменных
    parameters = symbols(' '.join(['a' + str(i) for i in range(len(func(x[0])))]))

    # Создание функции, представляющей собой линейную комбинацию заданных функций
    lin_comb = sum(coeff * term for coeff, term in zip(parameters, func(x[0])))

    # Конвертация символьной функции в функцию NumPy
    f = lambdify(parameters, lin_comb, modules='numpy')

    # Подготовка данных для метода наименьших квадратов
    x_data = np.array(x)
    y_data = np.array(y)
    A = np.array([func(xi) for xi in x_data])

    # Решение методом наименьших квадратов
    parameters_values, _ = lstsq(A, y_data, rcond=None)[:2]

    return tuple(parameters_values)


def expfit(x: list[float], y: list[float], g: list[float | int] = None) -> tuple[tuple, Callable[[float], tuple]]:
    """
    Экспоненциальная регрессия

    Функция expfit использует для минимизации метод Левенберга-Марквардта.
    Используйте функцию expfit, чтобы выполнить экспоненциальную регрессию.
    Экспоненциальные функции используются для всех процессов,
    которые затухают или нарастают до устойчивого состояния,
    таких как радиоактивный распад, нестационарный отклик RC-цепи
    или смещение сильно демпфированной пружины.

    f(x) = A * exp(b * x) + C

    :param x: вектор аргументов
    :param y: вектор значений
    :param g: трехэлементный вектор действительных приближенных значений
    для параметров A, b и C в экспоненциальном уравнении.
    Если этот аргумент не используется, то функция expfit генерирует приближение из линии,
    аппроксимирующей диаграмму вектора y.

    :return: кортеж коэффициентов и функция
    """
    if g is None:
        g = [1.0, 1.0, 1.0]

    x_data = np.array(x)
    y_data = np.array(y)

    # Выполнение подгонки к экспоненциальной функции с использованием метода Левенберга-Марквардта
    popt = curve_fit(
        lambda x, a, b, c: a * np.exp(b * x) + c,
        x_data,
        y_data,
        g,
    )[0]

    return tuple(popt), lambda x: popt[0] * np.exp(popt[1] * x) + popt[2]


def lgsfit(x: list[float], y: list[float], g: list[float | int] = None) -> tuple[tuple, Callable[[float], tuple]]:
    """
    Логистическая регрессия

    Функция lgsfit использует для минимизации метод Левенберга-Марквардта.
    Используйте функцию lgsfit, чтобы выполнить логистическую регрессию.
    Логистические функции используются для моделирования роста популяции,
    включая рост численности популяции в течение определенного периода времени,
    и для моделирования насыщения.

    f(x) = A / (1 + b * exp(-C * x))

    :param x: вектор аргументов
    :param y: вектор значений
    :param g: трехэлементный вектор действительных приближенных значений
    для параметров A, b и C в логистическом уравнении.

    return: кортеж коэффициентов и функция
    """
    if g is None:
        g = [1.0, 1.0, 1.0]

    x_data = np.array(x)
    y_data = np.array(y)

    # Выполнение подгонки к логистической функции с использованием метода Левенберга-Марквардта
    popt = curve_fit(
        lambda x, a, b, c: a / (1 + b * np.exp(-c * x)),
        x_data,
        y_data,
        g,
    )[0]

    return tuple(popt), lambda x: popt[0] / (1 + popt[1] * np.exp(-popt[2] * x))


def sinfit(x: list[float], y: list[float], g: list[float | int] = None) -> tuple[tuple, Callable[[float], tuple]]:
    """
    Синусоидальная регрессия

    Функция sinfit использует для минимизации метод Левенберга-Марквардта.
    Используйте функцию sinfit, чтобы выполнить синусоидальную регрессию.
    Синусоидальные функции используются для моделирования периодических процессов,
    таких как колебания волны, колебания в электрических цепях и колебания в механических системах.

    f(x) = A * sin(x + b) + C

    :param x: вектор аргументов
    :param y: вектор значений
    :param g: трехэлементный вектор действительных приближенных значений
    для параметров A, b и C в синусоидальном уравнении.

    return: кортеж коэффициентов и функция
    """
    if g is None:
        g = [1.0, 1.0, 1.0]

    x_data = np.array(x)
    y_data = np.array(y)

    # Выполнение подгонки к синусоидальной функции с использованием метода Левенберга-Марквардта
    popt = curve_fit(
        lambda x, a, b, c: a * np.sin(x + b) + c,
        x_data,
        y_data,
        g,
    )[0]

    return tuple(popt), lambda x: popt[0] * np.sin(x + popt[1]) + popt[2]


def pwrfit(x: list[float], y: list[float], g: list[float | int] = None) -> tuple[tuple, Callable[[float], tuple]]:
    """
    Степенная регрессия

    Функция pwrfit использует для минимизации метод Левенберга-Марквардта.
    Используйте функцию pwrfit, чтобы выполнить степенную регрессию.
    Степенные функции используются для моделирования процессов, которые увеличиваются или уменьшаются
    в зависимости от времени, таких как рост популяции, распространение болезни и распространение информации.

    f(x) = A * x^b + C

    :param x: вектор аргументов
    :param y: вектор значений
    :param g: трехэлементный вектор действительных приближенных значений
    для параметров A, b и C в степенном уравнении.

    return: кортеж коэффициентов и функция
    """
    if g is None:
        g = [1.0, 1.0, 1.0]

    x_data = np.array(x)
    y_data = np.array(y)

    # Выполнение подгонки к степенной функции с использованием метода Левенберга-Марквардта
    popt = curve_fit(
        lambda x, a, b, c: a * x ** b + c,
        x_data,
        y_data,
        g,
    )[0]

    return tuple(popt), lambda x: popt[0] * x ** popt[1] + popt[2]


def cspline(x: list[float], y: list[float]) -> np.ndarray[float]:
    """
    Кубический сплайн

    :param x: вектор аргументов
    :param y: вектор значений
    :return: vs вектор
    """

    x_data = np.array(x)
    y_data = np.array(y)

    cs = CubicSpline(x_data, y_data)
    return cs.x


def interp(vs: Sequence[float], vx: Sequence[float], vy: Sequence[float], x: float):
    """
    Функция interp в интерполяции и регрессии используется для интерполяции в данной точке
    выходных данных одной из следующих функций: cspline, lspline, pspline, bspline или loess.

    :param vs: Является вектором, созданным одной из следующих функций: cspline, lspline, pspline, bspline или loess.
    :param vx: Вектор аргументов
    :param vy: Вектор значений
    :param x: является вещественным значением независимой переменной,
    для которого требуется рассчитать кривую интерполяции.
    Для получения наилучших результатов это значение должно быть в диапазоне значений vx

    :return: Возвращает интерполированное значение в точке x из коэффициентов вектора vs и исходные данные в vx и vy.
    """
    x_data = np.array(vx)
    y_data = np.array(vy)

    return np.interp(x, x_data, y_data)