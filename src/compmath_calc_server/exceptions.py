from fastapi.exceptions import HTTPException as StarletteHTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response

from compmath_calc_server.models.error import Error, ErrorType, FieldErrorItem
from compmath_calc_server.views import BaseView


class APIError(StarletteHTTPException):
    def __init__(
            self,
            message: str = "Error",
            status_code: int = 400,
            headers: dict = None
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(status_code=status_code, headers=headers)


class NotFound(APIError):
    def __init__(self, message: str = "Запрашиваемый контент не найден") -> None:
        super().__init__(message=message, status_code=404)


class BadRequest(APIError):
    def __init__(self, message: str = "Неверный запрос") -> None:
        super().__init__(message=message, status_code=400)


def handle_api_error(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseView(
            error=Error(
                type=ErrorType.MESSAGE,
                content=exc.message
            )
        ).model_dump()
    )


def handle_pydantic_error(request: Request, exc: Exception | RequestValidationError) -> Response:
    content = []
    for error in exc.errors():
        field = error.get('loc', ['none'])[-1]
        location = error.get('loc', [])
        message = error.get('msg', 'No message')
        error_type = error.get('type', 'empty')

        if error_type == "missing":
            message = "Поле является обязательным"
        elif error_type == "value_error":
            message = ", ".join(error['ctx']['error'].args)

        content.append(
            FieldErrorItem(
                field=field,
                location=location,
                message=message,
                type=error_type
            )
        )

    return JSONResponse(
        status_code=400,
        content=BaseView(
            error=Error(
                type=ErrorType.FIELD_LIST,
                content=content
            )
        ).model_dump()
    )


def handle_404_error(request, exc):
    if isinstance(exc, NotFound):
        return handle_api_error(request, exc)

    return JSONResponse(
        status_code=exc.status_code,
        content=BaseView(
            error=Error(
                type=ErrorType.MESSAGE,
                content='Запрашиваемый контент не найден'
            )
        ).model_dump()
    )
