from dataclasses import dataclass
from typing import Callable, Sequence

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
    x_limits: tuple[float | int, float | int]
    color: str


class Graphic:
    def __init__(
            self,
            x_limits: tuple[float | int, float | int] = None
    ):
        self.x_limits = x_limits

        self.graphs = []

    def add_graph(
            self,
            fx: Callable[[float | int], float],
            *,
            color: str = 'blue',
            step: float | int = 0.1,
            x_limits: tuple[float | int, float | int] = None
    ) -> None:
        if not (x_limits or self.x_limits):
            raise ValueError("Не заданы пределы по X или Y")

        x_data = np.arange(
            x_limits[0] if x_limits else self.x_limits[0],
            x_limits[1] if x_limits else self.x_limits[1],
            step
        )

        y_data = np.array([fx(x) for x in x_data])

        graph = GraphModel(
            x_data=x_data,
            y_data=y_data,
            x_limits=x_limits,
            color=color
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
                plot_item = PlotDataItem(graph.x_data, graph.y_data, pen=pg.mkPen(graph.color))
            else:
                plot_item = PlotDataItem([graph.x], [graph.y], pen=None, symbol='o', symbolBrush=graph.color)
            plot_items.append(plot_item)
        return plot_items
