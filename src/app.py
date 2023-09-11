import os
import importlib
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.configs.config import settings

app = FastAPI()


def include_routers(dirname):
    for basedir, _, package_names in os.walk(dirname):
        for package_name in package_names:
            full_package_dir = f'{dirname}/{package_name}'
            full_package_name = full_package_dir[:-3].replace('/', '.')
            if full_package_name not in sys.modules:
                try:
                    route = importlib.import_module(full_package_name)
                    app.include_router(route.router)
                    print(f'Router included: {route}')
                except ModuleNotFoundError:
                    pass


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version="1.0.0",
        description=f"This is an OpenAPI for {settings.APP_NAME} API",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


include_routers('src/routes')
app.openapi = custom_openapi

if settings.HB_ENV == "development":
    uvicorn.run(app, host=settings.API_NODE, port=settings.API_PORT)
