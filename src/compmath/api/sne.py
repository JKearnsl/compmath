from typing import Any

import numpy as np
from PyQt6.QtCore import pyqtSignal

from compmath.api.base import APIBase, urljoin
from compmath.models.graphic import Graphic, PolygonModel, RectModel, GraphModel, PointModel
from compmath.models.sne.base import TableRow
from compmath.utils.data import dicts_to_dataclasses


class SNEClient(APIBase):
    simCalculated = pyqtSignal(object)
    ntmCalculated = pyqtSignal(object)
    zmCalculated = pyqtSignal(object)

    simError = pyqtSignal(str)
    ntmError = pyqtSignal(str)
    zmError = pyqtSignal(str)

    def calc_sim(
            self,
            equations: list[str],
            eps: float,
            iters_limit: int,
            initial_guess: tuple[int | float, int | float],
            x_limits: tuple[int | float, int | float],
            y_limits: tuple[int | float, int | float],
    ) -> None:
        """
        Вычисление метода простой итерации

        :param initial_guess: начальное приближение
        :param iters_limit: максимальное количество итераций
        :param eps: точность
        :param equations: уравнения
        :param points: отсортированный двумерный массив точек (x, y)
        :param x_limits: пределы по оси X
        :param y_limits: пределы по оси Y
        :return: список графиков, логов, результатов и названий моделей
        """
        self.post(
            urljoin(self._base_url, "/sne/sim/calculate"),
            {
                "equations": equations,
                "eps": eps,
                "iters_limit": iters_limit,
                "initial_guess": initial_guess,
                "x_limits": x_limits,
                "y_limits": y_limits
            },
            [lambda content: self._calculated(self.simCalculated, content)],
            [self.simError.emit]
        )

    def calc_ntm(
            self,
            equations: list[str],
            eps: float,
            iters_limit: int,
            initial_guess: tuple[int | float, int | float],
            x_limits: tuple[int | float, int | float],
            y_limits: tuple[int | float, int | float],
    ) -> None:
        """
        Вычисление метода Ньютона

        :param y_limits:
        :param initial_guess: начальное приближение
        :param iters_limit: максимальное количество итераций
        :param eps: точность
        :param equations: уравнения
        :param points: отсортированный двумерный массив точек (x, y)
        :param x_limits: пределы по оси X
        :return: список графиков, логов, результатов и названий моделей
        """
        self.post(
            urljoin(self._base_url, "/sne/ntm/calculate"),
            {
                "equations": equations,
                "eps": eps,
                "iters_limit": iters_limit,
                "initial_guess": initial_guess,
                "x_limits": x_limits,
                "y_limits": y_limits
            },
            [lambda content: self._calculated(self.ntmCalculated, content)],
            [self.ntmError.emit]
        )

    def calc_zm(
            self,
            equations: list[str],
            eps: float,
            iters_limit: int,
            initial_guess: tuple[int | float, int | float],
            x_limits: tuple[int | float, int | float],
            y_limits: tuple[int | float, int | float],
    ) -> None:
        """
        Вычисление метода Зейделя

        :param initial_guess: начальное приближение
        :param iters_limit: максимальное количество итераций
        :param eps: точность
        :param equations: уравнения
        :param points: отсортированный двумерный массив точек (x, y)
        :param x_limits: пределы по оси X
        :param y_limits: пределы по оси Y
        :return: список графиков, логов, результатов и названий моделей
        """
        self.post(
            urljoin(self._base_url, "/sne/zm/calculate"),
            {
                "equations": equations,
                "eps": eps,
                "iters_limit": iters_limit,
                "initial_guess": initial_guess,
                "x_limits": x_limits,
                "y_limits": y_limits
            },
            [lambda content: self._calculated(self.zmCalculated, content)],
            [self.zmError.emit]
        )

    def _calculated(self, signal: pyqtSignal, content: dict[str, Any]):
        graphics = []

        graphs = content['graphics']
        solve_log = content['solve_log']
        table = dicts_to_dataclasses(
            content['table'],
            [
                TableRow
            ]
        )

        for i, graph in enumerate(graphs):
            plot_items = dicts_to_dataclasses(
                graph,
                [
                    PolygonModel,
                    RectModel,
                    GraphModel,
                    PointModel
                ]
            )

            for item in plot_items:
                if isinstance(item, GraphModel):
                    if None in item.x_data:
                        for i, coord in enumerate(item.x_data):
                            if coord is None:
                                item.x_data[i] = np.nan
                    if None in item.y_data:
                        for i, coord in enumerate(item.y_data):
                            if coord is None:
                                item.y_data[i] = np.nan

            graphic = Graphic()
            graphic.graphs.extend(plot_items)
            graphics.append(graphic)

        signal.emit((graphics, solve_log, table))
