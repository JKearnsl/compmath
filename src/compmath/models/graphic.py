from collections import deque
from dataclasses import dataclass
from typing import Callable, Sequence, cast

import numpy as np
import pyqtgraph as pg
from pyqtgraph import PlotDataItem


@dataclass
class PointModel:
    x: float | int
    y: float | int
    color: str


@dataclass
class GraphModel:
    x_data: Sequence[float | int]
    y_data: Sequence[float | int]
    color: str
    width: float | int
    fill: str | None


@dataclass
class RectModel:
    x: float | int
    y: float | int
    x1: float | int
    y1: float | int
    color: str


class Graphic:
    def __init__(
            self,
            x_limits: tuple[float | int, float | int] = None,
            y_limits: tuple[float | int, float | int] = None
    ):
        self.x_limits = x_limits
        self.y_limits = y_limits

        self.graphs = deque()

    def add_graph(
            self,
            fx: Callable[[float | int], float] = None,
            fy: Callable[[float | int], float] = None,
            *,
            color: str = 'blue',
            step: float | int = 0.1,
            width: float | int = 1,
            fill: str | None = False,
            x_limits: tuple[float | int, float | int] = None,
            y_limits: tuple[float | int, float | int] = None
    ) -> None:

        x_limits = tuple(sorted(x_limits or self.x_limits))
        y_limits = tuple(sorted(y_limits or self.y_limits))

        if fx and not x_limits:
            raise ValueError("Не задан предел по X")

        if fy and not y_limits:
            raise ValueError("Не задан предел по Y")

        if fx:
            x_data = np.arange(
                x_limits[0],
                x_limits[1],
                step
            )
            if len(x_data) != 0 and x_data[-1] != x_limits[1]:
                x_data = np.append(x_data, x_limits[1])
            y_data = np.array([fx(x) for x in x_data])
            for i, el in enumerate(y_data):
                if cast(float, el) < y_limits[0] or cast(float, el) > y_limits[1]:
                    y_data[i] = np.nan
        elif fy:
            y_data = np.arange(
                y_limits[0],
                y_limits[1],
                step
            )
            if len(y_data) != 0 and y_data[-1] != y_limits[1]:
                y_data = np.append(y_data, y_limits[1])
            x_data = np.array([fy(y) for y in y_data])
        else:
            raise ValueError("Не задана функция")

        graph = GraphModel(
            x_data=x_data,
            y_data=y_data,
            color=color,
            width=width,
            fill=fill
        )
        self.graphs.append(graph)

    def add_point(
            self,
            x: int | float,
            y: int | float,
            color: str = 'red'
    ) -> None:
        self.graphs.append(PointModel(x=x, y=y, color=color))

    def plot_items(self) -> list[PlotDataItem]:
        plot_items = []
        for graph in self.graphs:
            if isinstance(graph, GraphModel):
                plot_item = PlotDataItem(
                    graph.x_data,
                    graph.y_data,
                    pen=pg.mkPen(
                        color=graph.color,
                        width=graph.width
                    ),
                    fillLevel=0 if graph.fill else None,
                    fillBrush=pg.mkBrush(graph.fill) if graph.fill else None
                )
            elif isinstance(graph, PointModel):
                plot_item = PlotDataItem(
                    [graph.x],
                    [graph.y],
                    pen=None,
                    symbol='o',
                    symbolBrush=graph.color
                )
            elif isinstance(graph, RectModel):
                plot_item = PlotDataItem(
                    [graph.x, graph.x, graph.x1, graph.x1, graph.x],
                    [graph.y, graph.y1, graph.y1, graph.y, graph.y],
                    pen=pg.mkPen(graph.color)
                )
            else:
                raise ValueError(f"Неизвестный тип графика {type(graph)}")
            plot_items.append(plot_item)
        return plot_items

    def show(self):
        """
        Debug method for show plot


        :return:
        """
        plot = pg.plot()
        for plot_item in self.plot_items():
            plot.addItem(plot_item)
        plot.show()
        return plot

    def add_rect(
            self,
            x: int | float,
            y: int | float,
            x1: int | float,
            y1: int | float,
            color: str = 'blue'
    ) -> None:
        self.graphs.append(
            RectModel(
                x=x,
                y=y,
                x1=x1,
                y1=y1,
                color=color
            )
        )
