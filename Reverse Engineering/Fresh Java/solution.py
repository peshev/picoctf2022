#!/usr/bin/env python3

import subprocess
import re

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

subprocess.check_output(["fernflower", "KeygenMe.class", "."])

with open("KeygenMe.java") as fp:
    java_code = list(map(str.strip, fp.readlines()))

flag = []
for line in java_code:
    match = re.match(r"}\s*else\s+if\s*\(var2.charAt\((\d+)\)\s*!=\s*'(.)'\s*\)\s*{", line)
    if match:
        flag.append((int(match.group(1)), match.group(2)))
print("".join(c for _, c in sorted(flag)))
