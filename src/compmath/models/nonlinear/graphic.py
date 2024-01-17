from dataclasses import dataclass
from typing import Callable, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


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
    y_limits: tuple[float | int, float | int]
    color: str


class Graphic:
    def __init__(
            self,
            y_limits: tuple[float | int, float | int] = None,
            x_limits: tuple[float | int, float | int] = None
    ):
        self.y_limits = y_limits
        self.x_limits = x_limits

        self.graphs = []

    def add_graph(
            self,
            fx: Callable[[float | int], float],
            *,
            color: str = 'blue',
            step: float | int = 0.1,
            y_limits: tuple[float | int, float | int] = None,
            x_limits: tuple[float | int, float | int] = None
    ) -> None:
        if not (y_limits or self.y_limits) or not (x_limits or self.x_limits):
            raise ValueError("Не заданы пределы по X или Y")

        x_data = np.arange(
            x_limits[0] if x_limits else self.x_limits[0],
            x_limits[1] if x_limits else self.x_limits[1],
            step
        )
        y_data = [fx(x) for x in x_data]

        graph = GraphModel(
            x_data=x_data,
            y_data=y_data,
            x_limits=x_limits,
            y_limits=y_limits,
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

    def canvas(self) -> FigureCanvasQTAgg:
        for graph in self.graphs:
            if isinstance(graph, GraphModel):
                plt.plot(graph.x_data, graph.y_data, color=graph.color)
                plt.xlim(graph.x_limits)
                plt.ylim(graph.y_limits)
            else:
                plt.scatter(graph.x, graph.y, color=graph.color)

        plt.grid(True)

        return FigureCanvasQTAgg(plt.gcf())
