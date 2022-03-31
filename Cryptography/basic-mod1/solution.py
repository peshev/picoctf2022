#!/usr/bin/env python3
import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

charset = [chr(ord('A') + i) for i in range(26)] + [chr(ord('0') + i) for i in range(10)] + ['_']
with open("message.txt") as fp:
    ciphertext = list(map(int, fp.read().strip().split()))

print("picoCTF{" + "".join(charset[i % len(charset)] for i in ciphertext) + "}")
