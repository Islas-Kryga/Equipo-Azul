"""Generación del banco de imágenes BMP para las pruebas del proyecto."""

import math
import os
import struct
from typing import Callable, List, Tuple


WIDTH = 300
HEIGHT = 300

Color = Tuple[int, int, int]
Shape = Tuple[Color, Callable[[int, int], bool]]

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)


def triangle(
    p1: Tuple[int, int],
    p2: Tuple[int, int],
    p3: Tuple[int, int],
) -> Callable[[int, int], bool]:
    """Crea la función de pertenencia para un triángulo."""
    def contains(x: int, y: int) -> bool:
        def sign(a, b, c):
            return (
                (a[0] - c[0]) * (b[1] - c[1])
                - (b[0] - c[0]) * (a[1] - c[1])
            )

        point = (x, y)
        d1 = sign(point, p1, p2)
        d2 = sign(point, p2, p3)
        d3 = sign(point, p3, p1)

        has_negative = d1 < 0 or d2 < 0 or d3 < 0
        has_positive = d1 > 0 or d2 > 0 or d3 > 0

        return not (has_negative and has_positive)

    return contains


def rectangle(
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> Callable[[int, int], bool]:
    """Crea la función de pertenencia para un rectángulo."""
    return lambda x, y: left <= x <= right and top <= y <= bottom


def polygon(points: List[Tuple[int, int]]) -> Callable[[int, int], bool]:
    """Crea la función de pertenencia para un polígono convexo."""
    def contains(x: int, y: int) -> bool:
        signs = []

        for i in range(len(points)):
            a = points[i]
            b = points[(i + 1) % len(points)]

            cross = (
                (b[0] - a[0]) * (y - a[1])
                - (b[1] - a[1]) * (x - a[0])
            )

            if cross != 0:
                signs.append(cross > 0)

        return not signs or all(sign == signs[0] for sign in signs)

    return contains


def circle(
    center_x: int,
    center_y: int,
    radius: int,
) -> Callable[[int, int], bool]:
    """Crea la función de pertenencia para un círculo."""
    return lambda x, y: (
        (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
    )


def create_bmp(path: str, shapes: List[Shape]) -> None:
    """Crea una imagen BMP de 24 bits con las figuras indicadas."""
    row_size = (WIDTH * 3 + 3) & ~3
    pixel_data = bytearray()

    for y in range(HEIGHT - 1, -1, -1):
        row = bytearray()

        for x in range(WIDTH):
            color = WHITE

            for shape_color, contains in shapes:
                if contains(x, y):
                    color = shape_color
                    break

            red, green, blue = color
            row.extend((blue, green, red))

        row.extend(b"\x00" * (row_size - WIDTH * 3))
        pixel_data.extend(row)

    file_size = 54 + len(pixel_data)

    header = struct.pack(
        "<2sIHHI",
        b"BM",
        file_size,
        0,
        0,
        54,
    )

    dib_header = struct.pack(
        "<IIIHHIIIIII",
        40,
        WIDTH,
        HEIGHT,
        1,
        24,
        0,
        len(pixel_data),
        2835,
        2835,
        0,
        0,
    )

    with open(path, "wb") as bmp_file:
        bmp_file.write(header)
        bmp_file.write(dib_header)
        bmp_file.write(pixel_data)


def generate_images() -> None:
    """Genera las diez imágenes que forman el banco de pruebas."""
    os.makedirs("imagenes", exist_ok=True)

    tests = [
        (
            "prueba01.bmp",
            [
                (RED, triangle((150, 40), (60, 240), (240, 240))),
            ],
        ),
        (
            "prueba02.bmp",
            [
                (BLUE, rectangle(70, 70, 230, 230)),
            ],
        ),
        (
            "prueba03.bmp",
            [
                (GREEN, circle(150, 150, 85)),
            ],
        ),
        (
            "prueba04.bmp",
            [
                (
                    MAGENTA,
                    polygon([
                        (150, 35),
                        (245, 105),
                        (210, 230),
                        (90, 245),
                        (40, 120),
                    ]),
                ),
            ],
        ),
        (
            "prueba05.bmp",
            [
                (RED, triangle((75, 60), (25, 210), (125, 210))),
                (BLUE, rectangle(170, 80, 270, 200)),
            ],
        ),
        (
            "prueba06.bmp",
            [
                (RED, triangle((55, 45), (15, 135), (95, 135))),
                (BLUE, rectangle(115, 40, 195, 120)),
                (GREEN, circle(245, 90, 42)),
            ],
        ),
        (
            "prueba07.bmp",
            [
                (
                    CYAN,
                    polygon([
                        (150, 35),
                        (265, 150),
                        (150, 265),
                        (35, 150),
                    ]),
                ),
            ],
        ),
        (
            "prueba08.bmp",
            [
                (RED, triangle((45, 25), (15, 90), (75, 90))),
                (BLUE, rectangle(105, 45, 255, 195)),
                (GREEN, circle(70, 220, 45)),
            ],
        ),
        (
            "prueba09.bmp",
            [
                (ORANGE, rectangle(0, 0, 75, 75)),
            ],
        ),
        (
            "prueba10.bmp",
            [
                (RED, triangle((50, 25), (10, 105), (90, 105))),
                (BLUE, rectangle(115, 25, 190, 100)),
                (GREEN, circle(250, 65, 38)),
                (
                    MAGENTA,
                    polygon([
                        (55, 165),
                        (100, 185),
                        (90, 245),
                        (45, 275),
                        (10, 225),
                    ]),
                ),
            ],
        ),
    ]

    for filename, shapes in tests:
        path = os.path.join("imagenes", filename)
        create_bmp(path, shapes)
        print(f"Imagen creada: {path}")


generate_images()