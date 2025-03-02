import os
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .settings import settings
from .utils.qr import generate_qr_svg

app = FastAPI()

static_file_path = os.path.dirname(os.path.realpath(__file__)) + "/static"
app.mount("/static", StaticFiles(directory=static_file_path), name="static")


@app.get("/", include_in_schema=False)
async def root():
    plausible_tag = ""
    if settings.plausible_domain:
        plausible_tag = f'<script defer data-domain="{settings.plausible_domain}" src="https://plausible.io/js/script.js"></script>'

    with open(static_file_path + "/index.html", "r") as f:
        content = f.read()
        content = content.replace("{{plausible_tag}}", plausible_tag)

    return Response(content=content, media_type="text/html")


class ImageStyles(str, Enum):
    circle: str = "circle"
    square: str = "square"


class ImageSchema(BaseModel):
    msg: str
    error_level: int = 15
    box_size: int = 100
    border: int = 0
    size_ratio: float = 0.8
    stencil: bool = True
    style: ImageStyles = "square"
    color: str = "black"
    background: str | None = None


@app.get(
    "/image.{format}",
    responses={200: {"content": {"image/svg": {}}}},
    response_class=Response,
)
async def qr_stencil(img_request: Annotated[ImageSchema, Query()], format: str):
    if format == "svg":
        stencil = generate_qr_svg(
            img_request.msg,
            error_level=img_request.error_level,
            box_size=img_request.box_size,
            border=img_request.border,
            size_ratio=img_request.size_ratio,
            stencil=img_request.stencil,
            style=img_request.style,
            color=img_request.color,
            background=img_request.background,
        )
        return Response(content=stencil, media_type="image/svg+xml")
    else:
        raise HTTPException(status_code=404, detail="Invalid format")
