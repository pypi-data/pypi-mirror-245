from __future__ import annotations

import importlib.resources
import os
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.templating import _TemplateResponse  # noqa: TCH002
from uvicorn import Config, Server

from . import __version__
from .actions import store_heartbeat_from_fitbit
from .graphs import get_heartbeat_graph


class SpaceActionEvent(BaseModel):
    event_id: Literal["store_data_from_fitbit"] = Field(alias="id")
    trigger: str


class SpaceAction(BaseModel):
    event: SpaceActionEvent


resource_root_path = Path(str(importlib.resources.files("heartbeat_status")))
app = FastAPI()
templates = Jinja2Templates(directory=resource_root_path / "templates")

app.mount("/static", StaticFiles(directory=resource_root_path / "static_files"))


@app.get("/fitbit/callback")
async def fitbit_callback(code: str, state: str) -> RedirectResponse:  # noqa: ARG001
    return RedirectResponse(url="/")


@app.api_route(
    "/healthcheck",
    methods=["GET", "HEAD"],
    status_code=status.HTTP_200_OK,
)
async def healthcheck() -> Response:
    return Response(content="OK", media_type="text/plain")


@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def root(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
        "index.j2",
        {"request": request, "version": __version__},
    )


@app.get("/graph/heartbeat")
async def heartbeat_graph() -> HTMLResponse:
    return HTMLResponse(content=get_heartbeat_graph(), status_code=200)


@app.api_route(
    "/__space/v0/actions",
    methods=["POST", "HEAD"],
)
async def space_actions(action: SpaceAction) -> Response:
    if action.event.event_id == "store_data_from_fitbit":
        store_heartbeat_from_fitbit()
        return Response(content="OK", media_type="text/plain")
    return Response(content="NG", media_type="text/plain", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


def main() -> None:
    config = Config(
        app,
        port=5000,
        log_level="info",
        reload=bool(os.environ.get("DEBUG")),
    )
    server = Server(config)
    server.run()


if __name__ == "__main__":
    main()
