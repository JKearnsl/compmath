from pydantic import BaseModel
from compmath_calc_server.models.graphic import GraphicItem


class InputNIModel(BaseModel):
    a: float
    b: float
    intervals: int
    fx: str
    x_limits: tuple[float, float]
    y_limits: tuple[float, float]


class InputNInterModel(BaseModel):
    a: float
    b: float
    fx: str
    x_limits: tuple[float, float]
    y_limits: tuple[float, float]


class TableRow(BaseModel):
    num: int
    x: float
    y: float
    value: float


class OutputNIModel(BaseModel):
    graphic_items: list[GraphicItem]
    table: list[TableRow]
    result: float


class OutputNInterModel(BaseModel):
    graphic_items: list[GraphicItem]
    reference_result: float
    surface_area: float
    volume: float
    arc_length: float
