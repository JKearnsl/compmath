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
