import os

from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles

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


@app.get(
    "/image.{format}",
    responses={200: {"content": {"image/svg": {}}}},
    response_class=Response,
)
async def qr_stencil(
    msg: str,
    format: str,
    error_level: int = 15,
    box_size: int = 100,
    border: int = 0,
    size_ratio: float = 0.8,
):
    if format == "svg":
        stencil = generate_qr_svg(
            msg,
            error_level=error_level,
            box_size=box_size,
            border=border,
            size_ratio=size_ratio,
        )
        return Response(content=stencil, media_type="image/svg+xml")
    else:
        raise HTTPException(status_code=404, detail="Invalid format")
