#!/usr/bin/env python3

import subprocess

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

bases = [(str.islower, 'a'), (str.isupper, 'A')]


def rot13(c):
    for f, b in bases:
        if f(c):
            return chr(ord(b) + (ord(c) - ord(b) + 13) % 26)
    return c


subprocess.check_call(["tar", "xf", "leak.tar"])
with open("leak/usernames.txt") as u, open("leak/passwords.txt") as p:
    _, password = next(
        iter(filter(lambda x: x[0] == "cultiris", zip(map(str.strip, u.readlines()), map(str.strip, p.readlines())))))

print("".join(map(rot13, password)))
