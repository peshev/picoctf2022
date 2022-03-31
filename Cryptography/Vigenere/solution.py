#!/usr/bin/env python3

import itertools

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

with open("cipher.txt", "r") as fp:
    cipher = fp.read().strip()

key = "CYLAB"
key = [ord('A') - ord(i) for i in key]

key_iter = iter(itertools.cycle(key))


def decrypt_character(c):
    if c.islower():
        base = 'a'
    elif c.isupper():
        base = 'A'
    else:
        return c

    return chr(ord(base) + (ord(c) - ord(base) + next(key_iter)) % 26)


print("".join(map(decrypt_character, cipher)))
