#!/usr/bin/env python3

import re

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

with open("message.txt", "r") as fp:
    message = fp.read()

first_three_ciphertext = message[:3]
first_three_plaintext = "The"
target_indexes = [
    first_three_ciphertext.index(c)
    for c in
    first_three_plaintext
]

flag = "".join(
    message[i:i + 3][t]
    for i in
    range(0, len(message), 3)
    for t in
    target_indexes
)

print(re.match("The flag is (picoCTF{.+})", flag).group(1))
