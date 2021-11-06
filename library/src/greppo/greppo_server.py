import logging
import os
from distutils.sysconfig import get_python_lib
from functools import partial

import uvicorn
from greppo import GreppoApp
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response
from starlette.routing import Mount
from starlette.routing import Route
from starlette.routing import WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from .user_script_utils import script_task

templates = Jinja2Templates(directory="templates")


async def api_endpoint(user_script: str, request: Request):
    input_updates = {}
    try:
        input_updates = await request.json()
        logging.debug("Got input update: ", input_updates)
    except Exception as e:
        logging.debug("Unable to parse request body: ", await request.body(), e)

    payload, _ = await script_task(script_name=user_script, input_updates=input_updates)

    return JSONResponse(payload)


async def raster_api_endpoint(user_script: str, request: Request):
    input_updates = {}
    try:
        input_updates = await request.json()
        logging.debug("Got input update: ", input_updates)
    except Exception as e:
        logging.debug("Unable to parse request body: ", await request.body(), e)

    _, payload = await script_task(script_name=user_script, input_updates=input_updates)

    image_bytes_data = payload.read() if payload else None

    return Response(content=image_bytes_data, media_type="image/png")


def get_static_dir_path():
    dist_path = get_python_lib() + "/greppo"
    if os.path.isfile(dist_path):
        BASE_DIR = dist_path
    else:
        BASE_DIR = os.path.dirname(__file__)

    return BASE_DIR + "/static/"


class GreppoServer(object):
    def __init__(self, gr_app: GreppoApp, user_script: str):
        self.gr_app = gr_app
        self.user_script = user_script

    def run(self, host="127.0.0.1", port=8000):
        routes = [
            Route(
                "/api", partial(api_endpoint, self.user_script), methods=["GET", "POST"]
            ),
            Route(
                "/raster",
                partial(raster_api_endpoint, self.user_script),
                methods=["GET", "POST"],
            ),
            WebSocketRoute("/ws", websocket_endpoint),
            Mount(
                "/",
                app=StaticFiles(directory=get_static_dir_path(), html=True),
                name="static",
            ),
        ]

        middleware = [
            Middleware(
                CORSMiddleware,
                allow_origins=[
                    "http://localhost:8080",
                    "http://127.0.0.1:8080",
                    "http://localhost:8000",
                    "http://127.0.0.1:8000",
                ],
                allow_methods=["GET", "POST"],
            )
        ]

        app = Starlette(debug=True, routes=routes, middleware=middleware)
        uvicorn.run(app, host=host, port=port)

    def close(self):
        pass


async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text("Hello, websocket!")
    await websocket.close()
