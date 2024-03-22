from typing import Any

import numpy as np
from PyQt6.QtCore import pyqtSignal

from compmath.api.base import APIBase, urljoin
from compmath.models.graphic import Graphic, PolygonModel, RectModel, GraphModel, PointModel
from compmath.models.sne.base import TableRow
from compmath.utils.data import dicts_to_dataclasses


class SLATClient(APIBase):
    simCalculated = pyqtSignal(object)
    zmCalculated = pyqtSignal(object)
    gmCalculated = pyqtSignal(object)

    simError = pyqtSignal(str)
    zmError = pyqtSignal(str)
    gmError = pyqtSignal(str)

    def calc_sim(
            self,
            a_matrix: list[list[float]],
            b_vector: list[float],
            eps: float,
            iters_limit: int,
            x0: list[float] | None = None,

    ) -> None:
        """
        Вычисление метода простой итерации

        :param x0: начальное приближение
        :param iters_limit: максимальное количество итераций
        :param eps: точность
        :param b_vector: вектор B
        :param a_matrix: матрица A
        :return: список графиков, логов, результатов и названий моделей
        """
        self.post(
            urljoin(self._base_url, "/slat/sim/calculate"),
            {
                "a_matrix": a_matrix,
                "b_vector": b_vector,
                "eps": eps,
                "iters_limit": iters_limit,
                "x0": x0
            },
            [lambda content: self._calculated(self.simCalculated, content)],
            [self.simError.emit]
        )

    def calc_zm(
            self,
            a_matrix: list[list[float]],
            b_vector: list[float],
            eps: float,
            iters_limit: int,
            x0: list[float] | None = None,

    ) -> None:
        """
        Вычисление метода Зейделя

        :param x0: начальное приближение
        :param iters_limit: максимальное количество итераций
        :param eps: точность
        :param b_vector: вектор B
        :param a_matrix: матрица A
        :return: список графиков, логов, результатов и названий моделей
        """
        self.post(
            urljoin(self._base_url, "/slat/zm/calculate"),
            {
                "a_matrix": a_matrix,
                "b_vector": b_vector,
                "eps": eps,
                "iters_limit": iters_limit,
                "x0": x0
            },
            [lambda content: self._calculated(self.zmCalculated, content)],
            [self.zmError.emit]
        )

    def calc_gm(
            self,
            a_matrix: list[list[float]],
            b_vector: list[float],
            eps: float,
            iters_limit: int,
            x0: list[float] | None = None,

    ) -> None:
        """
        Вычисление метода Гаусса-Зейделя

        :param x0: начальное приближение
        :param iters_limit: максимальное количество итераций
        :param eps: точность
        :param b_vector: вектор B
        :param a_matrix: матрица A
        :return: список графиков, логов, результатов и названий моделей
        """
        self.post(
            urljoin(self._base_url, "/slat/gm/calculate"),
            {
                "a_matrix": a_matrix,
                "b_vector": b_vector,
                "eps": eps,
                "iters_limit": iters_limit,
                "x0": x0
            },
            [lambda content: self._calculated(self.gmCalculated, content)],
            [self.gmError.emit]
        )

    def _calculated(self, signal: pyqtSignal, content: list[tuple[list[str], list[dict], str]]):
        results = []

        for row in content:
            table = dicts_to_dataclasses(
                row[1],
                [
                    TableRow
                ]
            )
            results.append((row[0], table, row[2]))

        signal.emit(results)
