import io
import struct
import unittest

from src.bmp_reader import BmpReader
from src.exceptions import BmpFormatError
from src.models import Point


def make_bmp(width, height, rows, bits_per_pixel=24):
    bytes_per_pixel = bits_per_pixel // 8
    row_size = ((width * bytes_per_pixel + 3) // 4) * 4
    pixel_data = bytearray()
    for row in reversed(rows):
        encoded = bytearray()
        for red, green, blue in row:
            encoded.extend((blue, green, red))
            if bits_per_pixel == 32:
                encoded.append(255)
        encoded.extend(b"\x00" * (row_size - len(encoded)))
        pixel_data.extend(encoded)
    offset = 54
    file_size = offset + len(pixel_data)
    file_header = struct.pack("<2sIHHI", b"BM", file_size, 0, 0, offset)
    info_header = struct.pack(
        "<IiiHHIIiiII",
        40,
        width,
        height,
        1,
        bits_per_pixel,
        0,
        len(pixel_data),
        0,
        0,
        0,
        0,
    )
    return file_header + info_header + pixel_data


class BmpReaderTests(unittest.TestCase):
    def test_reads_24_bit_bmp_and_keeps_top_left_origin(self):
        image = BmpReader().read_stream(
            io.BytesIO(
                make_bmp(
                    2,
                    3,
                    [
                        [(255, 0, 0), (0, 255, 0)],
                        [(0, 0, 255), (255, 255, 255)],
                        [(10, 20, 30), (40, 50, 60)],
                    ],
                )
            )
        )

        self.assertEqual((255, 0, 0), image.pixel_at(Point(0, 0)))
        self.assertEqual((255, 255, 255), image.pixel_at(Point(1, 1)))
        self.assertEqual((40, 50, 60), image.pixel_at(Point(1, 2)))

    def test_rejects_invalid_signature(self):
        data = bytearray(make_bmp(1, 1, [[(0, 0, 0)]]))
        data[0:2] = b"ZZ"

        with self.assertRaises(BmpFormatError):
            BmpReader().read_stream(io.BytesIO(data))

    def test_rejects_unsupported_bit_depth(self):
        with self.assertRaises(BmpFormatError):
            BmpReader().read_stream(
                io.BytesIO(make_bmp(1, 1, [[(0, 0, 0)]], bits_per_pixel=32)[:28] + b"\x00" * 26)
            )


if __name__ == "__main__":
    unittest.main()
