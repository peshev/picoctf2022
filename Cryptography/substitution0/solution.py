#!/usr/bin/env python3

import re

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

with open("message.txt") as fp:
    lines = list(map(str.strip, fp.readlines()))
key = lines[0]

for line in lines[2:]:
    decrypted_line = ""
    for c in line:
        if c.isupper():
            d = chr(ord('A') + key.index(c))
        elif c.islower():
            d = chr(ord('a') + key.index(c.upper()))
        else:
            d = c
        decrypted_line += d
    match = re.search("picoCTF{.+?}", decrypted_line)
    if match:
        print(match.group(0))
