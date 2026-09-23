"""Excepciones específicas de la lectura y representación de imágenes BMP."""


class BmpError(Exception):
    """Error base para problemas relacionados con una imagen BMP."""


class BmpFormatError(BmpError):
    """La imagen no cumple con el subconjunto BMP soportado."""


class BmpFileError(BmpError):
    """No fue posible abrir o leer el archivo BMP."""
