#!/usr/bin/env python3

# Copyright © 2022 Pontus Lurcock

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# “Software”), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Print the lon/lat of a specified photo

Currently very quick-and-dirty and barely tested.

Might be extended to something more capable at some point.
"""


from typing import Any
import sys
from PIL import Image
import piexif


def main():
    img = Image.open(sys.argv[1])
    exif = piexif.load(img.info["exif"])
    gps = GPS(exif['GPS'])
    print(gps.lon(), gps.lat())


class GPS:

    def __init__(self, gps_dict: dict):
        self.gps_dict = gps_dict
        self.lon_dir = gps_dict.get(1, None).decode('utf-8')
        self.lon_pos = gps_dict.get(2, None)
        self.lat_dir = gps_dict.get(3, None).decode('utf-8')
        self.lat_pos = gps_dict.get(4, None)
        self.unknown = gps_dict.get(5, None)
        self.altitude = gps_dict.get(6, None)
        self.timestamp = gps_dict.get(7, None)
        self.direction_ref = gps_dict.get(16, None)
        self.direction = gps_dict.get(17, None)
        self.datestamp = gps_dict.get(29, None)

    def lon(self) -> float:
        return self.to_decimal_degrees(self.lon_pos)

    def lat(self) -> float:
        return self.to_decimal_degrees(self.lat_pos)

    @staticmethod
    def to_decimal_degrees(d) -> float:
        return (
            d[0][0] / d[0][1] +
            d[1][0] / (d[1][1] * 60) +
            d[2][0] / (d[2][1] * 3600)
        )


if __name__ == "__main__":
    main()
