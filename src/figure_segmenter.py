"""Segmentación de figuras geométricas mediante BFS."""

from collections import Counter, deque
from typing import List, Set

from .models import BmpImage, BoundingBox, FigureRegion, Point, RgbColor


class FigureSegmenter:
    """
    Detecta el color de fondo y separa cada figura conectada
    utilizando búsqueda en anchura (BFS).
    """

    def __init__(self, image: BmpImage) -> None:
        self.image = image
        self.background_color: RgbColor = self._detect_background_color()

    def _detect_background_color(self) -> RgbColor:
        """
        Determina el color de fondo muestreando el perímetro exterior completo de la imagen.
        Tomando el caso de la existencia de figuras en las esquinas. El color más repetido 
        en los bordes exteriores será el fondo.
        """
        w, h = self.image.width, self.image.height
        border_colors = []

        # 1. Filas superior e inferior
        for x in range(w):
            border_colors.append(self.image.pixel_at(Point(x, 0)))
            border_colors.append(self.image.pixel_at(Point(x, h - 1)))

        # 2. Columnas izquierda y derecha (sin repetir las esquinas)
        for y in range(1, h - 1):
            border_colors.append(self.image.pixel_at(Point(0, y)))
            border_colors.append(self.image.pixel_at(Point(w - 1, y)))

        color_counts = Counter(border_colors)
        most_common_color, _ = color_counts.most_common(1)[0]
        return most_common_color

    def segment(self) -> List[FigureRegion]:
        """
        Escanea la imagen completa y extrae cada componente conexa (figura).
        """
        visited: Set[Point] = set()
        figures: List[FigureRegion] = []

        for y in range(self.image.height):
            for x in range(self.image.width):
                pt = Point(x, y)
                if pt in visited:
                    continue

                color = self.image.pixel_at(pt)
                if color == self.background_color:
                    visited.add(pt)
                    continue

                region = self._bfs_flood(pt, color, visited)
                figures.append(region)

        return figures

    def _bfs_flood(
        self, start: Point, target_color: RgbColor, visited: Set[Point]
    ) -> FigureRegion:
        queue = deque([start])
        visited.add(start)

        figure_pixels: Set[Point] = set()
        min_x, max_x = start.x, start.x
        min_y, max_y = start.y, start.y

        # Vecindad-4: arriba, abajo, izquierda, derecha
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while queue:
            current = queue.popleft()
            figure_pixels.add(current)

            if current.x < min_x: min_x = current.x
            if current.x > max_x: max_x = current.x
            if current.y < min_y: min_y = current.y
            if current.y > max_y: max_y = current.y

            for dx, dy in offsets:
                nx, ny = current.x + dx, current.y + dy

                if 0 <= nx < self.image.width and 0 <= ny < self.image.height:
                    neighbor = Point(nx, ny)
                    if neighbor not in visited:
                        if self.image.pixel_at(neighbor) == target_color:
                            visited.add(neighbor)
                            queue.append(neighbor)

        bounds = BoundingBox(left=min_x, top=min_y, right=max_x, bottom=max_y)
        return FigureRegion(
            color=target_color,
            pixels=frozenset(figure_pixels),
            bounds=bounds,
        )