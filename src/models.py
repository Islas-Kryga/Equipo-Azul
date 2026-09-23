"""Modelos compartidos entre los módulos del reconocedor."""

from dataclasses import dataclass
from typing import Iterator, Sequence, Tuple

RgbColor = Tuple[int, int, int]


@dataclass(frozen=True, order=True)
class Point:
    """Coordenada de un píxel; el origen está en la esquina superior izquierda."""

    x: int
    y: int


@dataclass(frozen=True)
class BoundingBox:
    """Rectángulo mínimo que contiene una región de píxeles."""

    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self) -> int:
        return self.right - self.left + 1

    @property
    def height(self) -> int:
        return self.bottom - self.top + 1


@dataclass(frozen=True)
class FigureRegion:
    """Región conectada que una etapa posterior puede analizar y clasificar."""

    color: RgbColor
    pixels: frozenset[Point]
    bounds: BoundingBox

    @property
    def area(self) -> int:
        return len(self.pixels)


class BmpImage:
    """Imagen inmutable en memoria con colores RGB de 8 bits por canal."""

    def __init__(
        self,
        width: int,
        height: int,
        pixels: Sequence[Sequence[RgbColor]],
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Las dimensiones de la imagen deben ser positivas.")
        if len(pixels) != height or any(len(row) != width for row in pixels):
            raise ValueError("La matriz de píxeles no coincide con las dimensiones.")

        normalized = []
        for row in pixels:
            normalized_row = []
            for color in row:
                if len(color) != 3 or any(not 0 <= channel <= 255 for channel in color):
                    raise ValueError("Cada color debe ser una tupla RGB válida.")
                normalized_row.append(tuple(color))
            normalized.append(tuple(normalized_row))

        self._width = width
        self._height = height
        self._pixels = tuple(normalized)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def pixel_at(self, point: Point) -> RgbColor:
        """Devuelve el color en una coordenada o falla si está fuera de la imagen."""
        if not 0 <= point.x < self.width or not 0 <= point.y < self.height:
            raise IndexError("La coordenada está fuera de los límites de la imagen.")
        return self._pixels[point.y][point.x]

    def rows(self) -> Iterator[Tuple[RgbColor, ...]]:
        """Itera las filas de arriba hacia abajo."""
        return iter(self._pixels)

    def colors(self) -> Iterator[Tuple[Point, RgbColor]]:
        """Itera cada coordenada junto con su color RGB."""
        for y, row in enumerate(self._pixels):
            for x, color in enumerate(row):
                yield Point(x, y), color
