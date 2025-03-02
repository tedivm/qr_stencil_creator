import decimal
from io import BytesIO

import qrcode
import qrcode.image.svg as qr_svg
from qrcode.compat.etree import ET
from qrcode.image.styles.moduledrawers.svg import (
    SvgCircleDrawer,
    SvgPathCircleDrawer,
    SvgPathSquareDrawer,
    SvgSquareDrawer,
)

error_levels = {
    7: qrcode.constants.ERROR_CORRECT_L,
    15: qrcode.constants.ERROR_CORRECT_M,
    25: qrcode.constants.ERROR_CORRECT_Q,
    30: qrcode.constants.ERROR_CORRECT_H,
}

default_factory = qr_svg.SvgImage

styles = {
    qr_svg.SvgImage: {
        "square": SvgSquareDrawer,
        "circle": SvgCircleDrawer,
    },
    qr_svg.SvgPathImage: {
        "square": SvgPathSquareDrawer,
        "circle": SvgPathCircleDrawer,
    },
}


class NullDrawer(SvgSquareDrawer):
    def drawrect(self, box, is_active: bool):
        return


def add_eyes(img: qr_svg.SvgImage, size_ratio: float):
    for corner in ["top_left", "top_right", "bottom_left"]:
        draw_eye(img, corner, img.box_size, img.border, size_ratio)


def draw_eye(img, corner, unit_size, border_size, size_ratio):

    if corner == "top_left":
        start_x = border_size
        start_y = border_size
    elif corner == "top_right":
        start_x = (img.pixel_size - (unit_size * 7)) - border_size
        start_y = border_size
    elif corner == "bottom_left":
        start_x = border_size
        start_y = (img.pixel_size - (unit_size * 7)) - border_size
    else:
        raise ValueError("Invalid corner")

    buffer = img.width - int(size_ratio * img.width)

    # Top Line
    img._img.append(
        ET.Element(
            ET.QName(img._SVG_namespace, "rect"),
            x=img.units(float(start_x)),
            y=img.units(float(start_y)),
            width=img.units(float(unit_size) * 7),
            height=img.units(float(unit_size)),
        )
    )

    # Bottom Line
    img._img.append(
        ET.Element(
            ET.QName(img._SVG_namespace, "rect"),
            x=img.units(float(start_x)),
            y=img.units(float(start_y + (unit_size * 6))),
            width=img.units(float(unit_size) * 7),
            height=img.units(float(unit_size)),
        )
    )

    # Left Line
    img._img.append(
        ET.Element(
            ET.QName(img._SVG_namespace, "rect"),
            x=img.units(float(start_x)),
            y=img.units(float(start_y + unit_size + buffer)),
            width=img.units(float(unit_size)),
            height=img.units((float(unit_size) * 5) - (buffer * 2)),
        )
    )

    # Right Line
    img._img.append(
        ET.Element(
            ET.QName(img._SVG_namespace, "rect"),
            x=img.units(float(start_x + (unit_size * 6))),
            y=img.units(float(start_y + unit_size + buffer)),
            width=img.units(float(unit_size)),
            height=img.units((float(unit_size) * 5) - (buffer * 2)),
        )
    )

    # Square
    img._img.append(
        ET.Element(
            ET.QName(img._SVG_namespace, "rect"),
            x=img.units(float(start_x + (unit_size * 2))),
            y=img.units(float(start_y + (unit_size * 2))),
            width=img.units(float(unit_size) * 3),
            height=img.units(float(unit_size) * 3),
        )
    )


def generate_qr_svg(
    data: str,
    error_level: int = 15,
    box_size: int = 100,
    border: int = 0,
    size_ratio: float = 0.8,
    stencil: bool = True,
    style: str = "square",
    eye_drawer=None,
    factory_class=default_factory,
):

    drawer_class = styles.get(factory_class, {}).get(style, None)
    if drawer_class is None:
        raise ValueError(
            f"Invalid style {style} factory class {factory_class.__name__}"
        )
    module_drawer = drawer_class(size_ratio=decimal.Decimal(size_ratio))

    if error_level not in error_levels:
        raise ValueError("Invalid error level")
    error_correction = error_levels[error_level]

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        image_factory=factory_class,
    )
    qr.add_data(data)

    img = qr.make_image(
        module_drawer=module_drawer,
        eye_drawer=NullDrawer(),
    )

    stencil_ratio = size_ratio if stencil else 1
    add_eyes(img, stencil_ratio)

    stream = BytesIO()
    img.save(stream)

    return stream.getvalue().decode()
