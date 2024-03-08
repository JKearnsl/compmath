import logging
from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError

from compmath_calc_server.controllers import sne, ni
from compmath_calc_server.controllers import aif
from compmath_calc_server.config import load_config
from compmath_calc_server.exceptions import APIError, handle_api_error, handle_404_error, handle_pydantic_error
from compmath_calc_server.utils.openapi import custom_openapi


def create_app():
    config = load_config()
    logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO)
    app = FastAPI(
        title="Compmath Calc Server API",
        debug=config.DEBUG,
        version=config.VERSION,
        docs_url="/docs",
        redoc_url=None,
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    )

    app.openapi = lambda: custom_openapi(app)

    # Обработчики
    api_router = APIRouter(prefix="/api")
    api_router.include_router(aif.router, prefix="/aif", tags=["AIF"])
    api_router.include_router(sne.router, prefix="/sne", tags=["SNE"])
    api_router.include_router(ni.router, prefix="/ni", tags=["NI"])
    app.include_router(api_router)

    logging.debug("Регистрация обработчиков исключений")
    app.add_exception_handler(APIError, handle_api_error)
    app.add_exception_handler(404, handle_404_error)
    app.add_exception_handler(RequestValidationError, handle_pydantic_error)

    logging.debug("Приложение успешно создано")

    return app


application = create_app()
