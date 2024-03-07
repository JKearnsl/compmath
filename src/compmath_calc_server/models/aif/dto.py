from pydantic import BaseModel
from compmath_calc_server.models.graphic import GraphicItem


class InputAIFModel(BaseModel):
    points: list[tuple[float, float]]
    y_limits: tuple[float, float] = (-10, 10)
    x_limits: tuple[float, float] = (-10, 10)

    class Config:
        json_schema_extra = {
            "example": {
                "points": [(1, 1), (2, 2)],
                "y_limits": (-10, 10),
                "x_limits": (-10, 10)
            }
        }


class ResultAIFItem(BaseModel):
    log: list[str]
    sum_diff: float | None
    coefficient: float | None
    graphic_items: list[GraphicItem]
    title: str

    class Config:
        json_schema_extra = {
            "example": {
                "log": ["log1", "log2"],
                "sum_diff": 1.0,
                "coefficient": 1.0,
                "graphic_items": [{"x": 1, "y": 1, "color": "red"}],
                "title": "Some Method"
            }
        }


class InputInterpModel(BaseModel):
    points: list[tuple[float, float]]
    x: float
    y_limits: tuple[float, float] = (-10, 10)
    x_limits: tuple[float, float] = (-10, 10)

    class Config:
        json_schema_extra = {
            "example": {
                "points": [(1, 1), (2, 2)],
                "x": 1,
                "y_limits": (-10, 10),
                "x_limits": (-10, 10)
            }
        }


class ResultInterpItem(BaseModel):
    log: list[str]
    graphic_items: list[GraphicItem]
    title: str

    class Config:
        json_schema_extra = {
            "example": {
                "log": ["log1", "log2"],
                "graphic_items": [{"x": 1, "y": 1, "color": "red"}],
                "title": "Some Method"
            }
        }
