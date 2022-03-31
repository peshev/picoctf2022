#!/usr/bin/env python3

import re
from PIL import Image

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()


def img_to_pixel_matrix(filename):
    img = Image.open(filename)
    width, _ = img.size
    imgdata = list(img.convert("RGBA").getdata())
    return [imgdata[i:i + width] for i in range(0, len(imgdata), width)]


def pixel_matrix_to_bitstream(pixels, bitmask=0x01, channels=(0, 1, 2)):
    return [
        pixel[channel] & bitmask
        for row in
        pixels
        for pixel in
        row
        for channel in
        channels
    ]


def bitstream_to_bytes(bits):
    result = []
    i = 0
    byte = 0
    for bit in bits:
        byte <<= 1
        byte |= bit
        i += 1
        if i == 8:
            result.append(byte)
            byte = 0
            i = 0
    return bytes(result)


print(
    re.match(
        b"picoCTF{.+?}",
        bitstream_to_bytes(
            pixel_matrix_to_bitstream(
                img_to_pixel_matrix("pico.flag.png")))
    ).group(0).decode()
)
