"""Clasifica las figuras."""

from .figure_result import FigureResult


class ShapeClassifier:
    """Clasifica una figura como C, T, O o X."""

    def classify(self, figure, features):
        if features["is_circle"]:
            category = "O"

        elif features["corners"] == 3:
            category = "T"

        elif features["corners"] == 4:
            category = "C"

        else:
            category = "X"

        return FigureResult(
            category=category,
            color=figure.color,
        )