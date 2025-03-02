import typer

from qr_stencil.utils.qr import generate_qr_svg

from .settings import settings

app = typer.Typer()


@app.command(help="Generate a QR Code SVG with customizable options.")
def generate(
    msg: str,
    output: str,
    error_level: int = 15,
    box_size: int = 100,
    border: int = 0,
    size_ratio: float = 0.8,
):
    svg_content = generate_qr_svg(
        msg,
        error_level=error_level,
        box_size=box_size,
        border=border,
        size_ratio=size_ratio,
    )
    with open(output, "w") as f:
        f.write(svg_content)
    typer.echo(f"QR code generated and saved to {output}")


@app.command(help=f"Display the current installed version of {settings.project_name}.")
def version():
    from . import _version

    typer.echo(f"{settings.project_name} - {_version.version}")


if __name__ == "__main__":
    app()
