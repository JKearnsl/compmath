from fastapi.openapi.utils import get_openapi


def custom_openapi(app, logo_url: str = None):
    if not app.openapi_schema:
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']

        openapi_schema["info"]["x-logo"] = {
            "url": logo_url
        }
        app.openapi_schema = openapi_schema
    return app.openapi_schema
