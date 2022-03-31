#!/usr/bin/env python3
import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()


def find_mod_inv(a, m):
    for x in range(1, m):
        if (a % m) * (x % m) % m == 1:
            return x


charset = [chr(ord('A') + i) for i in range(26)] + [chr(ord('0') + i) for i in range(10)] + ['_']
with open("message.txt") as fp:
    ciphertext = list(map(int, fp.read().strip().split()))

print("picoCTF{" + "".join(charset[find_mod_inv(i, 41) - 1] for i in ciphertext) + "}")
