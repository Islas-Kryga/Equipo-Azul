"""Lectura de imágenes BMP sin dependencias externas."""

import struct
from typing import BinaryIO, List, Optional

from .exceptions import BmpFileError, BmpFormatError
from .models import BmpImage, RgbColor


class BmpReader:
    """Lee BMP sin compresión de 24 o 32 bits por píxel."""

    _FILE_HEADER_SIZE = 14
    _INFO_HEADER_SIZE = 40

    def read(self, path: str) -> BmpImage:
        """Lee una ruta y devuelve la imagen normalizada en RGB."""
        try:
            with open(path, "rb") as stream:
                return self.read_stream(stream)
        except FileNotFoundError as error:
            raise BmpFileError(f"No existe el archivo BMP: {path}") from error
        except OSError as error:
            raise BmpFileError(f"No se pudo abrir el archivo BMP: {path}") from error

    def read_stream(self, stream: BinaryIO) -> BmpImage:
        """Lee un flujo binario abierto en modo lectura."""
        file_header = self._read_exact(stream, self._FILE_HEADER_SIZE)
        signature, _, _, _, pixel_offset = struct.unpack("<2sIHHI", file_header)
        if signature != b"BM":
            raise BmpFormatError("El archivo no tiene la firma BMP 'BM'.")

        info_header = self._read_exact(stream, self._INFO_HEADER_SIZE)
        (
            header_size,
            width,
            signed_height,
            planes,
            bits_per_pixel,
            compression,
            image_size,
            _x_pixels_per_meter,
            _y_pixels_per_meter,
            _colors_used,
            _important_colors,
        ) = struct.unpack("<IiiHHIIiiII", info_header)

        if header_size < self._INFO_HEADER_SIZE:
            raise BmpFormatError("La cabecera DIB es demasiado pequeña.")
        if width <= 0 or signed_height == 0:
            raise BmpFormatError("Las dimensiones BMP no son válidas.")
        if planes != 1:
            raise BmpFormatError("Un BMP válido debe tener un solo plano de color.")
        if bits_per_pixel not in (24, 32):
            raise BmpFormatError("Solo se soportan imágenes BMP de 24 o 32 bits.")
        if compression != 0:
            raise BmpFormatError("Solo se soportan BMP sin compresión.")

        if header_size > self._INFO_HEADER_SIZE:
            self._read_exact(stream, header_size - self._INFO_HEADER_SIZE)
        stream.seek(pixel_offset)

        height = abs(signed_height)
        bytes_per_pixel = bits_per_pixel // 8
        row_size = ((width * bytes_per_pixel + 3) // 4) * 4
        rows: List[Optional[List[RgbColor]]] = [None] * height

        for file_row in range(height):
            row_data = self._read_exact(stream, row_size)
            row = [
                (row_data[index + 2], row_data[index + 1], row_data[index])
                for index in range(0, width * bytes_per_pixel, bytes_per_pixel)
            ]
            y = file_row if signed_height < 0 else height - file_row - 1
            rows[y] = row

        # El formato BMP guarda normalmente la primera fila al final.
        image_rows = []
        for row in rows:
            if row is None:
                raise BmpFormatError("No se pudo reconstruir una fila de píxeles.")
            image_rows.append(row)
        return BmpImage(width, height, image_rows)

    @staticmethod
    def _read_exact(stream: BinaryIO, size: int) -> bytes:
        data = stream.read(size)
        if len(data) != size:
            raise BmpFormatError("El archivo BMP está incompleto.")
        return data
