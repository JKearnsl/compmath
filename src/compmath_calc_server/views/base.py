from typing import Any

from pydantic import BaseModel

from compmath_calc_server.models.error import Error


class BaseView(BaseModel):
    content: Any = None
    error: Error = None
