#!/usr/bin/env python3

from collections import Counter

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

words_filename = "words.txt"
with open(words_filename, "r") as fp:
    words = fp.read()
characters = [c.lower() for c in words if c.isalpha()]
counts = Counter(characters)
print(sorted([(round(v / len(characters) * 100, 2), k) for k, v in counts.items()], reverse=True))
