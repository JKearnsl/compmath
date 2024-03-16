from collections import deque
from typing import Callable, cast

import numpy as np
from pydantic import BaseModel


class PointModel(BaseModel):
    x: float | int
    y: float | int
    color: str


class GraphModel(BaseModel):
    x_data: list[float | None]
    y_data: list[float | None]
    color: str
    width: float | int
    fill: str | None


class RectModel(BaseModel):
    x1: float | int
    y1: float | int
    x2: float | int
    y2: float | int
    color: str
    width: float | int
    fill: str | None


class PolygonModel(BaseModel):
    points: list[tuple[float | int, float | int]]
    color: str
    width: float | int
    fill: str | None


class MeshModel(BaseModel):
    vertexes: list[list[float]]
    faces: list[list[int]]
    shader: str


type GraphicItem = PointModel | GraphModel | RectModel | PolygonModel | MeshModel


class GraphicBuilder:
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
            fill: str | None = None,
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
            ).tolist()
            if len(x_data) != 0 and x_data[-1] != x_limits[1]:
                x_data.append(x_limits[1])

            y_data = cast(list[float | None], [fx(x) for x in x_data])
            for i, el in enumerate(y_data):
                if cast(float, el) < y_limits[0] or cast(float, el) > y_limits[1] or np.isnan(el):
                    y_data[i] = None
        elif fy:
            y_data = np.arange(
                y_limits[0],
                y_limits[1],
                step
            ).tolist()
            if len(y_data) != 0 and y_data[-1] != y_limits[1]:
                y_data.append(y_limits[1])

            x_data = cast(list[float | None], [fy(y) for y in y_data])
            for i, el in enumerate(x_data):
                if cast(float, el) < x_limits[0] or cast(float, el) > x_limits[1] or np.isnan(el):
                    x_data[i] = None
        else:
            raise ValueError("Не задана функция")

        graph = GraphModel(
            x_data=list(x_data),
            y_data=list(y_data),
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
        return self.graphs.append(
            PointModel(
                x=x,
                y=y,
                color=color
            )
        )

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
            points: list[tuple[float | int, float | int]],
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

    def add_mesh(
            self,
            vertexes: list[list[float]],
            faces: list[list[int]],
            shader: str = "normalColor"
    ) -> None:
        self.graphs.append(
            MeshModel(
                vertexes=vertexes,
                faces=faces,
                shader=shader
            )
        )

    def build(self) -> list[GraphicItem]:
        return list(self.graphs)
