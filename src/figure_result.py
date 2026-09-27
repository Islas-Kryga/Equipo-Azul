"""Modelo para representar el resultado de una figura reconocida."""

from dataclasses import dataclass

from .models import RgbColor


@dataclass(frozen=True)
class FigureResult:
    """Representa la categoría y el color de una figura reconocida."""

    category: str
    color: RgbColor

    def __post_init__(self) -> None:
        """Valida que la categoría sea una de las definidas por el proyecto."""
        if self.category not in {"C", "T", "O", "X"}:
            raise ValueError(
                "La categoría debe ser 'C', 'T', 'O' o 'X'."
            )