import decimal
from io import BytesIO

import qrcode
import qrcode.image.svg
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

default_factory = qrcode.image.svg.SvgImage

styles = {
    qrcode.image.svg.SvgImage: {
        "square": SvgSquareDrawer,
        "circle": SvgCircleDrawer,
    },
    qrcode.image.svg.SvgPathImage: {
        "square": SvgPathSquareDrawer,
        "circle": SvgPathCircleDrawer,
    },
}


class EyeDrawer(SvgSquareDrawer):
    def __init__(
        self, *, size_ratio: decimal.Decimal | float = decimal.Decimal(1), **kwargs
    ):
        self.size_ratio = decimal.Decimal(1)
        self.eye_size_ratio = float(size_ratio)

    def stencil_el(self, box):
        coords = self.coords(box)
        return ET.Element(
            self.tag_qname,  # type: ignore
            x=self.img.units(coords.x0),
            y=self.img.units(coords.y0),
            width=self.unit_size,
            height=self.img.units(float(self.box_size) * float(self.eye_size_ratio)),
        )

    def drawrect(self, box, is_active: bool):
        if not is_active:
            return

        coords = self.get_grid_position(box)
        get_cut_grids = self.get_cut_grids()

        if coords in get_cut_grids:
            self.img._img.append(self.stencil_el(box))
        else:
            self.img._img.append(self.el(box))

    def get_grid_position(self, box):
        top_left_x = box[0][0]
        top_left_y = box[0][1]

        x = (top_left_x - self.img.border) / self.img.box_size
        y = (top_left_y - self.img.border) / self.img.box_size

        return (int(x), int(y))

    def get_cut_grids(self):
        cut_grids = [
            # Top Left
            (0, 1),
            (0, 5),
            (6, 1),
            (6, 5),
            # Top Right
            (self.img.width - 7, 1),
            (self.img.width - 7, 5),
            (self.img.width - 1, 1),
            (self.img.width - 1, 5),
            # Bottom Left
            (0, self.img.width - 6),
            (0, self.img.width - 2),
            (6, self.img.width - 6),
            (6, self.img.width - 2),
        ]
        return cut_grids


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

    eye_drawer = None
    if stencil:
        eye_drawer = EyeDrawer(size_ratio=decimal.Decimal(size_ratio))

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
        eye_drawer=eye_drawer,
    )

    stream = BytesIO()
    img.save(stream)

    return stream.getvalue().decode()
