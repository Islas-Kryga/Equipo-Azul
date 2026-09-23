"""Pruebas unitarias para el segmentador de figuras."""

import unittest
from src.models import BmpImage, Point
from src.figure_segmenter import FigureSegmenter


class TestFigureSegmenter(unittest.TestCase):

    def test_single_figure_segmented(self):
        bg = (255, 255, 255)
        red = (255, 0, 0)

        # Matriz de 4x4 con un cuadrado rojo de 2x2 en el centro
        pixels = [
            [bg,  bg,  bg,  bg],
            [bg, red, red,  bg],
            [bg, red, red,  bg],
            [bg,  bg,  bg,  bg],
        ]
        image = BmpImage(4, 4, pixels)
        segmenter = FigureSegmenter(image)
        figures = segmenter.segment()

        self.assertEqual(len(figures), 1)
        fig = figures[0]
        self.assertEqual(fig.color, (255, 0, 0))
        self.assertEqual(fig.area, 4)
        self.assertEqual(fig.bounds.left, 1)
        self.assertEqual(fig.bounds.top, 1)
        self.assertEqual(fig.bounds.right, 2)
        self.assertEqual(fig.bounds.bottom, 2)

    def test_multiple_figures_and_background_detection(self):
        bg = (0, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)

        pixels = [
            [bg,   bg,   bg,   bg,   bg],
            [bg, blue,   bg, green,  bg],
            [bg, blue,   bg, green,  bg],
            [bg,   bg,   bg,   bg,   bg],
        ]
        image = BmpImage(5, 4, pixels)
        segmenter = FigureSegmenter(image)
        figures = segmenter.segment()

        self.assertEqual(len(figures), 2)
        colors_found = {f.color for f in figures}
        self.assertIn(blue, colors_found)
        self.assertIn(green, colors_found)


if __name__ == "__main__":
    unittest.main()