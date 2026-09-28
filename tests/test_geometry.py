import math
import unittest

from src.geometry_analyzer import GeometryAnalyzer
from src.models import BoundingBox, FigureRegion, Point
from src.shape_classifier import ShapeClassifier


def make_figure(points, color=(255, 0, 0)):
    """Crea una FigureRegion a partir de una lista de puntos."""

    pixels = frozenset(
        Point(x, y)
        for x, y in points
    )

    xs = [point.x for point in pixels]
    ys = [point.y for point in pixels]

    bounds = BoundingBox(
        min(xs),
        min(ys),
        max(xs),
        max(ys),
    )

    return FigureRegion(
        color,
        pixels,
        bounds,
    )


def polygon_pixels(vertices):
    """Obtiene los píxeles que están dentro de un polígono."""

    min_x = math.floor(
        min(x for x, y in vertices)
    )
    max_x = math.ceil(
        max(x for x, y in vertices)
    )
    min_y = math.floor(
        min(y for x, y in vertices)
    )
    max_y = math.ceil(
        max(y for x, y in vertices)
    )

    result = []

    def inside(x, y):
        inside_polygon = False
        j = len(vertices) - 1

        for i in range(len(vertices)):
            xi, yi = vertices[i]
            xj, yj = vertices[j]

            if (yi > y) != (yj > y):
                intersection = (
                    (xj - xi) * (y - yi) / (yj - yi)
                    + xi
                )

                if x < intersection:
                    inside_polygon = not inside_polygon

            j = i

        return inside_polygon

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if inside(x + 0.5, y + 0.5):
                result.append((x, y))

    return result


def circle_pixels(radius):
    """Genera los píxeles de un círculo."""

    pixels = []

    for y in range(-radius, radius + 1):
        for x in range(-radius, radius + 1):
            if x * x + y * y <= radius * radius:
                pixels.append((x, y))

    return pixels


def rotated_rectangle(
    center_x,
    center_y,
    width,
    height,
    angle_degrees,
):
    """Genera los píxeles de un rectángulo rotado."""

    angle = math.radians(angle_degrees)

    vertices = []

    for sx, sy in [
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2),
    ]:
        x = (
            center_x
            + sx * math.cos(angle)
            - sy * math.sin(angle)
        )

        y = (
            center_y
            + sx * math.sin(angle)
            + sy * math.cos(angle)
        )

        vertices.append((round(x), round(y)))

    return polygon_pixels(vertices)


class GeometryAnalyzerTests(unittest.TestCase):

    def setUp(self):
        self.analyzer = GeometryAnalyzer()

    def test_detects_triangle(self):
        points = polygon_pixels([
            (10, 40),
            (40, 40),
            (25, 10),
        ])

        figure = make_figure(points)

        features = self.analyzer.analyze(figure)

        self.assertEqual(3, features["corners"])
        self.assertFalse(features["is_circle"])

    def test_detects_rectangle(self):
        points = polygon_pixels([
            (10, 10),
            (70, 10),
            (70, 40),
            (10, 40),
        ])

        figure = make_figure(points)

        features = self.analyzer.analyze(figure)

        self.assertEqual(4, features["corners"])
        self.assertFalse(features["is_circle"])

    def test_detects_rotated_rectangle(self):
        points = rotated_rectangle(
            50,
            50,
            60,
            30,
            45,
        )

        figure = make_figure(points)

        features = self.analyzer.analyze(figure)

        self.assertEqual(4, features["corners"])
        self.assertFalse(features["is_circle"])

    def test_detects_rhombus(self):
        points = polygon_pixels([
            (40, 10),
            (70, 35),
            (40, 60),
            (10, 35),
        ])

        figure = make_figure(points)

        features = self.analyzer.analyze(figure)

        self.assertEqual(4, features["corners"])
        self.assertFalse(features["is_circle"])

    def test_detects_trapezoid(self):
        points = polygon_pixels([
            (20, 10),
            (60, 10),
            (70, 50),
            (10, 50),
        ])

        figure = make_figure(points)

        features = self.analyzer.analyze(figure)

        self.assertEqual(4, features["corners"])
        self.assertFalse(features["is_circle"])

    def test_detects_small_circle(self):
        points = circle_pixels(10)

        figure = make_figure(points)

        features = self.analyzer.analyze(figure)

        self.assertTrue(features["is_circle"])

    def test_detects_medium_circle(self):
        points = circle_pixels(15)

        figure = make_figure(points)

        features = self.analyzer.analyze(figure)

        self.assertTrue(features["is_circle"])

    def test_detects_large_circle(self):
        points = circle_pixels(30)

        figure = make_figure(points)

        features = self.analyzer.analyze(figure)

        self.assertTrue(features["is_circle"])

    def test_pentagon_is_not_triangle_or_quadrilateral(self):
        vertices = []

        for i in range(5):
            angle = math.radians(-90 + i * 72)

            x = 50 + 30 * math.cos(angle)
            y = 50 + 30 * math.sin(angle)

            vertices.append((x, y))

        points = polygon_pixels(vertices)

        figure = make_figure(points)

        features = self.analyzer.analyze(figure)

        self.assertNotIn(
            features["corners"],
            (3, 4),
        )


class ShapeClassifierTests(unittest.TestCase):

    def setUp(self):
        self.classifier = ShapeClassifier()

        self.figure = make_figure(
            [(0, 0)],
            color=(10, 20, 30),
        )

    def test_classifies_triangle_as_T(self):
        features = {
            "corners": 3,
            "is_circle": False,
        }

        result = self.classifier.classify(
            self.figure,
            features,
        )

        self.assertEqual("T", result.category)

    def test_classifies_quadrilateral_as_C(self):
        features = {
            "corners": 4,
            "is_circle": False,
        }

        result = self.classifier.classify(
            self.figure,
            features,
        )

        self.assertEqual("C", result.category)

    def test_classifies_circle_as_O(self):
        features = {
            "corners": 8,
            "is_circle": True,
        }

        result = self.classifier.classify(
            self.figure,
            features,
        )

        self.assertEqual("O", result.category)

    def test_classifies_other_as_X(self):
        features = {
            "corners": 5,
            "is_circle": False,
        }

        result = self.classifier.classify(
            self.figure,
            features,
        )

        self.assertEqual("X", result.category)

    def test_keeps_figure_color(self):
        features = {
            "corners": 3,
            "is_circle": False,
        }

        result = self.classifier.classify(
            self.figure,
            features,
        )

        self.assertEqual(
            (10, 20, 30),
            result.color,
        )


if __name__ == "__main__":
    unittest.main()