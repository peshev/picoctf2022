#!/usr/bin/env python3

import subprocess
import re

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

with open("unpackme.flag.py") as fp:
    code = fp.read()

code = re.sub(r"exec\(plain.decode\(\)\)", "print(plain.decode())", code)

with open("unpackme.flag.py.patched", "w") as fp:
    fp.write(code)

decrypted = subprocess.check_output(["python", "unpackme.flag.py.patched"]).decode()

with open("unpackme.flag.py.decrypted", "w") as fp:
    fp.write(decrypted)

print(re.search("picoCTF{.+}", decrypted).group(0))
