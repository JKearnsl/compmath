from pydantic import BaseModel


class InputSLATModel(BaseModel):
    a_matrix: list[list[float]]
    b_vector: list[float]
    eps: float
    iters_limit: int
    x0: list[float] | None = None


class TableRow(BaseModel):
    iter_num: int
    vector: list[int | float]
    delta: float

