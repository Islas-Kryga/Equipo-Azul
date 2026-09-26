"""Analiza la forma de una figura."""

import math

from .models import Point


class GeometryAnalyzer:
    """Obtiene caracateristicas de geometricas de un figura"""

    def analyze(self, figure):
        pixels = list(figure.pixels)

        boundary = self._get_boundary(pixels)
        hull = self._convex_hull(pixels)

        width = figure.bounds.width
        height = figure.bounds.height

        epsilon = max(width, height) * 0.03
        corners = self._simplify(hull, epsilon)

        return {
            "corners": len(corners),
            "is_circle": self._is_circle(
                pixels,
                boundary,
                width,
                height,
            ),
        }

    def _get_boundary(self, pixels):
        """Obtiene los píxeles que están en el borde."""

        pixel_set = set(pixels)
        boundary = []

        for pixel in pixels:
            neighbors = [
                Point(pixel.x + 1, pixel.y),
                Point(pixel.x - 1, pixel.y),
                Point(pixel.x, pixel.y + 1),
                Point(pixel.x, pixel.y - 1),
            ]

            if any(neighbor not in pixel_set for neighbor in neighbors):
                boundary.append(pixel)

        return boundary

    def _convex_hull(self, pixels):
        """Obtiene el borde exterior de la figura."""

        points = sorted(
            (pixel.x, pixel.y)
            for pixel in pixels
        )

        if len(points) <= 1:
            return points

        def cross(a, b, c):
            return (
                (b[0] - a[0]) * (c[1] - a[1])
                - (b[1] - a[1]) * (c[0] - a[0])
            )

        lower = []

        for point in points:
            while (
                len(lower) >= 2
                and cross(lower[-2], lower[-1], point) <= 0
            ):
                lower.pop()

            lower.append(point)

        upper = []

        for point in reversed(points):
            while (
                len(upper) >= 2
                and cross(upper[-2], upper[-1], point) <= 0
            ):
                upper.pop()

            upper.append(point)

        return lower[:-1] + upper[:-1]

    def _simplify(self, polygon, epsilon):
       
        polygon = polygon[:]

        changed = True

        while changed and len(polygon) > 3:
            changed = False

            for i in range(len(polygon)):
                a = polygon[i - 1]
                b = polygon[i]
                c = polygon[(i + 1) % len(polygon)]

                distance = self._distance_to_line(a, b, c)

                if distance < epsilon:
                    polygon.pop(i)
                    changed = True
                    break

        return polygon

    def _distance_to_line(self, a, b, c):
        """Distancia de b a la línea que une a y c."""

        denominator = math.sqrt(
            (c[0] - a[0]) ** 2
            + (c[1] - a[1]) ** 2
        )

        if denominator == 0:
            return 0

        numerator = abs(
            (b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0])
        )

        return numerator / denominator

    def _is_circle(self, pixels, boundary, width, height):
        """Comprueba si la figura tiene forma circular."""

        if not boundary:
            return False

        # Un círculo debe tener aproximadamente el mismo ancho
        # y alto.
        if abs(width - height) > 1:
            return False

        center_x = (
            min(pixel.x for pixel in pixels)
            + max(pixel.x for pixel in pixels)
        ) / 2

        center_y = (
            min(pixel.y for pixel in pixels)
            + max(pixel.y for pixel in pixels)
        ) / 2

        distances = []

        for pixel in boundary:
            distance = math.sqrt(
                (pixel.x - center_x) ** 2
                + (pixel.y - center_y) ** 2
            )

            distances.append(distance)

        average = sum(distances) / len(distances)

        if average == 0:
            return False

        variance = sum(
            (distance - average) ** 2
            for distance in distances
        ) / len(distances)

        variation = math.sqrt(variance) / average

        return variation < 0.02