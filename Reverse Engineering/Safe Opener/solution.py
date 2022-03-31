#!/usr/bin/env python3

import re
import base64

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

with open("SafeOpener.java", "r") as fp:
    java_code = fp.read()

flag = base64.b64decode(re.search('encodedkey = "([0-9A-Za-z]+)";', java_code).group(1)).decode()

print(f"picoCTF{{{flag}}}")
