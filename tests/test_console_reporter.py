"""Pruebas unitarias para la presentación de resultados en terminal."""

import io
import unittest
from contextlib import redirect_stdout

from src.console_reporter import ConsoleReporter
from src.figure_result import FigureResult


class ConsoleReporterTests(unittest.TestCase):
    """Verifica el comportamiento de ConsoleReporter."""

    def test_rgb_to_hex(self):
        """Comprueba la conversión de colores RGB a hexadecimal."""
        reporter = ConsoleReporter()

        self.assertEqual("#FF0000", reporter._rgb_to_hex((255, 0, 0)))
        self.assertEqual("#00FF00", reporter._rgb_to_hex((0, 255, 0)))
        self.assertEqual("#0000FF", reporter._rgb_to_hex((0, 0, 255)))

    def test_report_displays_figure(self):
        """Comprueba que se muestre la categoría y el color de una figura."""
        reporter = ConsoleReporter()
        result = FigureResult("C", (255, 0, 0))
        output = io.StringIO()

        with redirect_stdout(output):
            reporter.report([result])

        text = output.getvalue()

        self.assertIn("Figuras encontradas: 1", text)
        self.assertIn("Categoría: C", text)
        self.assertIn("Color: #FF0000", text)


if __name__ == "__main__":
    unittest.main()