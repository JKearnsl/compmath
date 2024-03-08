from pydantic import BaseModel
from compmath_calc_server.models.graphic import GraphicItem


class InputSNEModel(BaseModel):
    equations: list[str]
    eps: float
    iters_limit: int
    initial_guess: tuple[int | float, int | float]
    x_limits: tuple[int | float, int | float]
    y_limits: tuple[int | float, int | float]


class TableRow(BaseModel):
    iter_num: int
    vector: tuple[float, float]
    delta: float


class OutputSNEModel(BaseModel):
    solve_log: list[str]
    graphics: list[list[GraphicItem]]
    table: list[TableRow]
