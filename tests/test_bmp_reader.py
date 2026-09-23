import io
import struct
import unittest

from src.bmp_reader import BmpReader
from src.exceptions import BmpFileError, BmpFormatError
from src.models import BmpImage, BoundingBox, FigureRegion, Point


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

    def test_rejects_16_bit_bmp(self):
        with self.assertRaises(BmpFormatError):
            BmpReader().read_stream(
                io.BytesIO(make_bmp(1, 1, [[(0, 0, 0)]], bits_per_pixel=16))
            )

    def test_reports_missing_file_with_a_specific_error(self):
        with self.assertRaises(BmpFileError):
            BmpReader().read("archivo-que-no-existe.bmp")


class BmpImageTests(unittest.TestCase):
    def test_rejects_pixels_with_wrong_dimensions(self):
        with self.assertRaises(ValueError):
            BmpImage(2, 1, [[(0, 0, 0)]])

    def test_rejects_color_channels_outside_rgb_range(self):
        with self.assertRaises(ValueError):
            BmpImage(1, 1, [[(256, 0, 0)]])

    def test_exposes_regions_with_their_area_and_dimensions(self):
        pixels = frozenset({Point(1, 2), Point(2, 2), Point(1, 3)})
        region = FigureRegion((10, 20, 30), pixels, BoundingBox(1, 2, 2, 3))

        self.assertEqual(3, region.area)
        self.assertEqual(2, region.bounds.width)
        self.assertEqual(2, region.bounds.height)


if __name__ == "__main__":
    unittest.main()
