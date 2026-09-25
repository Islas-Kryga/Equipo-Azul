"""Presentación de los resultados del reconocimiento en la terminal."""

from typing import Iterable

from .figure_result import FigureResult
from .models import RgbColor


class ConsoleReporter:
    """Muestra en la terminal las figuras reconocidas y sus colores."""

    @staticmethod
    def _rgb_to_hex(color: RgbColor) -> str:
        """Convierte un color RGB a su representación hexadecimal."""
        red, green, blue = color
        return f"#{red:02X}{green:02X}{blue:02X}"

    def report(self, results: Iterable[FigureResult]) -> None:
        """Imprime de forma clara los resultados de las figuras reconocidas."""
        figures = list(results)

        print(f"Figuras encontradas: {len(figures)}")

        for index, result in enumerate(figures, start=1):
            print()
            print(f"Figura {index}")
            print(f"Categoría: {result.category}")
            print(f"Color: {self._rgb_to_hex(result.color)}")