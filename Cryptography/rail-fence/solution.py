#!/usr/bin/env python3

import math
import re

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()


def split_into_rails(ciphertext, outer_row_length):
    inner_row_length = 2 * outer_row_length - 1
    return (
            [ciphertext[:outer_row_length]] +
            [
                ciphertext[i:i + inner_row_length]
                for i in
                range(
                    outer_row_length,
                    len(ciphertext) - outer_row_length,
                    inner_row_length
                )
            ] +
            [ciphertext[-outer_row_length + 1:]]
    )


def rail_indexes(n, k):
    for i in range(k):
        yield 0, i
        for r in range(1, n - 1):
            yield r, i * 2
        yield n - 1, i
        for r in range(n - 2, 0, -1):
            yield r, i * 2 + 1


with open("message.txt") as fp:
    ciphertext = fp.read().strip()

rail_count = 4
outer_row_length = math.ceil(len(ciphertext) / (2 * (rail_count - 1)))
rails = split_into_rails(ciphertext, outer_row_length)
plaintext = "".join(
    rails[r][i]
    for r, i in
    rail_indexes(rail_count, outer_row_length)
    if i < len(rails[r])
).strip()
flag = re.match("^The flag is: (.+)$", plaintext).group(1)
print(f"picoCTF{{{flag}}}")
