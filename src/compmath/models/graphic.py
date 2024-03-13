from collections import deque
from dataclasses import dataclass
from typing import Callable, Sequence, cast

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPicture, QPainter, QPolygonF
from pyqtgraph import PlotDataItem
from pyqtgraph.opengl import GLSurfacePlotItem


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
    x1: float | int
    y1: float | int
    x2: float | int
    y2: float | int
    color: str
    width: float | int
    fill: str | None


@dataclass
class SurfaceModel:
    x: Sequence[float | int]
    y: Sequence[float | int]
    z: Sequence[float | int]
    shader: str
    color: tuple[float, float, float, float]


@dataclass
class PolygonModel:
    points: Sequence[tuple[float | int, float | int] | QPointF]
    color: str
    width: float | int
    fill: str | None


class RectItem(pg.GraphicsObject):
    def __init__(self, rect: QRectF, pen: pg.mkPen = None, brush: pg.mkBrush = None):
        super().__init__()
        if not pen:
            self.pen = pg.mkPen(
                color='red',
                width=1
            )
        else:
            self.pen = pen
        self.brush = brush
        self.picture = QPicture()
        self._rect = rect
        self._generate_picture()

    @property
    def rect(self):
        return self._rect

    def _generate_picture(self):
        painter = QPainter(self.picture)
        painter.setPen(self.pen)
        if self.brush:
            painter.setBrush(self.brush)
        painter.drawRect(self.rect)
        painter.end()

    def paint(self, painter, option, widget=None):
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

    def getData(self) -> tuple[Sequence[float | int], Sequence[float | int]]:
        return self.rect.x(), self.rect.y()


class PolygonItem(pg.GraphicsObject):
    def __init__(self, points: QPolygonF, pen=None, brush=None):
        super().__init__()
        if not pen:
            self.pen = pg.mkPen(
                color='red',
                width=1
            )
        else:
            self.pen = pen
        self.picture = QPicture()
        self.points = points
        self.brush = brush
        self._generate_picture()

    def _generate_picture(self):
        painter = QPainter(self.picture)
        painter.setPen(self.pen)
        if self.brush:
            painter.setBrush(self.brush)
        painter.drawPolygon(self.points)
        painter.end()

    def paint(self, painter, option, widget=None):
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

    def getData(self) -> tuple[Sequence[float | int], Sequence[float | int]]:
        return self.rect.x(), self.rect.y()


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
                plot_item = RectItem(
                    QRectF(
                        graph.x1,
                        graph.y1,
                        graph.x2 - graph.x1,
                        graph.y2 - graph.y1
                    ),
                    pen=pg.mkPen(
                        color=graph.color,
                        width=graph.width
                    ),
                    brush=pg.mkBrush(graph.fill) if graph.fill else None
                )
            elif isinstance(graph, PolygonModel):
                plot_item = PolygonItem(
                    QPolygonF([
                        QPointF(*point) for point in graph.points
                    ]),
                    pen=pg.mkPen(
                        color=graph.color,
                        width=graph.width
                    ),
                    brush=pg.mkBrush(graph.fill) if graph.fill else None
                )
            elif isinstance(graph, SurfaceModel):
                plot_item = GLSurfacePlotItem(
                    x=graph.x,
                    y=graph.y,
                    z=graph.z,
                    shader=graph.shader,
                    color=graph.color
                )
                plot_item.scale(16. / 49., 16. / 49., 1.0)
                plot_item.translate(-3, -3, 0)
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
            x1: int | float,
            y1: int | float,
            x2: int | float,
            y2: int | float,
            color: str = 'blue',
            width: int | float = 1,
            fill: str | None = None
    ) -> None:
        self.graphs.append(
            RectModel(
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                color=color,
                width=width,
                fill=fill
            )
        )

    def add_polygon(
            self,
            points: Sequence[tuple[float | int, float | int] | QPointF],
            color: str = 'blue',
            width: int | float = 1,
            fill: str | None = None
    ) -> None:
        self.graphs.append(
            PolygonModel(
                points=points,
                color=color,
                width=width,
                fill=fill
            )
        )

    def add_surface(
            self,
            x: Sequence[float | int],
            y: Sequence[float | int],
            z: Sequence[float | int],
            shader: str = 'shaded',
            color: tuple[float, float, float, float] = (0.5, 0.5, 0.5, 1)
    ) -> None:
        self.graphs.append(
            SurfaceModel(
                x=x,
                y=y,
                z=z,
                shader=shader,
                color=color
            )
        )
