"""Punto de entrada del reconocedor de figuras geométricas."""

import sys

from .bmp_reader import BmpReader
from .console_reporter import ConsoleReporter
from .exceptions import BmpError
from .figure_segmenter import FigureSegmenter
from .geometry_analyzer import GeometryAnalyzer
from .shape_classifier import ShapeClassifier


def main() -> int:
    """Ejecuta el flujo completo de reconocimiento de figuras."""

    if len(sys.argv) != 2:
        print("Uso: python -m src.main <ruta_imagen.bmp>")
        return 1

    image_path = sys.argv[1]

    try:
        image = BmpReader().read(image_path)
        figures = FigureSegmenter(image).segment()

        analyzer = GeometryAnalyzer()
        classifier = ShapeClassifier()
        results = []

        for figure in figures:
            features = analyzer.analyze(figure)
            result = classifier.classify(figure, features)
            results.append(result)

        ConsoleReporter().report(results)

    except BmpError as error:
        print(f"Error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
