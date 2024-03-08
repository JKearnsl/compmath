from typing import Any

import numpy as np
from PyQt6.QtCore import pyqtSignal

from compmath.api.base import APIBase, urljoin
from compmath.models.graphic import Graphic, PolygonModel, RectModel, GraphModel, PointModel
from compmath.utils.data import dicts_to_dataclasses


class AIFClient(APIBase):
    alsmCalculated = pyqtSignal(object)
    alsmError = pyqtSignal(str)
    interpCalculated = pyqtSignal(object)
    interpError = pyqtSignal(str)

    def calc_alsm(
            self,
            points: list[tuple[float | int, float | int]],
            x_limits: tuple[float | int, float | int],
            y_limits: tuple[float | int, float | int]
    ) -> None:
        """
        Вычисление всех моделей аппроксимации

        :param points: отсортированный двумерный массив точек (x, y)
        :param x_limits: пределы по оси X
        :param y_limits: пределы по оси Y
        :return: список графиков, логов, результатов и названий моделей
        """
        self.post(
            urljoin(self._base_url, "/aif/alsm/calculate"),
            {
                "points": points,
                "x_limits": x_limits,
                "y_limits": y_limits
            },
            [self._alsm_calculated],
            [self.alsmError.emit]
        )

    def calc_interp(
            self,
            points: list[tuple[float | int, float | int]],
            x_limits: tuple[float | int, float | int],
            y_limits: tuple[float | int, float | int],
            x: float | int
    ) -> None:
        """
        Вычисление всех моделей интерполяции

        :param points: отсортированный двумерный массив точек (x, y)
        :param x_limits: пределы по оси X
        :param y_limits: пределы по оси Y
        :param x: значение X
        :return: список графиков, логов, результатов и названий моделей
        """
        self.post(
            urljoin(self._base_url, "/aif/interp/calculate"),
            {
                "points": points,
                "x_limits": x_limits,
                "y_limits": y_limits,
                "x": x
            },
            [self._interp_calculated],
            [self.interpError.emit]
        )

    def _interp_calculated(self, content: list[dict[str, Any]]):
        result = []
        for el in content:
            graphs = el['graphic_items']
            logs = el['log']
            title = el['title']
            plot_items = dicts_to_dataclasses(
                graphs,
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

            result.append((graphic, logs, title))
        self.interpCalculated.emit(result)

    def _alsm_calculated(self, content: list[dict[str, Any]]):
        result = []
        for el in content:
            graphs = el['graphic_items']
            logs = el['log']
            results = (el['sum_diff'], el["coefficient"])
            title = el['title']
            plot_items = dicts_to_dataclasses(
                graphs,
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
            if results[1] is None:
                results = (results[0], np.nan)

            if results[0] is None:
                results = (np.nan, results[1])


            graphic = Graphic()
            graphic.graphs.extend(plot_items)

            result.append((graphic, logs, results, title))
        self.alsmCalculated.emit(result)
