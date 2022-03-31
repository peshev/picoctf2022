#!/usr/bin/env python3

import re
from subprocess import Popen, PIPE

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

with open("bloat.flag.py") as fp:
    code = [l.rstrip("\n") for l in fp.readlines()]

a_code = "\n".join(code[1:3])
exec(a_code)


def deobfuscate(s):
    return '"' + "".join(a[int(re.match(r"a\[(\d+)]", i).group(1))] for i in s.group(0).split("+")) + '"'


code = "\n".join(code)
code = re.sub(r"a\[\d+](?:\+a\[\d+])*", deobfuscate, code)
code = re.sub(r'"\+\s*\\\n\s*"', "", code)

with open("bloat.flag.py.deobfuscated", "w") as fp:
    fp.write(code)

password = re.search('if arg432 == "(.+)":', code).group(1)

p = Popen(['python', "bloat.flag.py"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
stdout_data = p.communicate(input=password.encode() + b"\n")[0].decode()

print(re.search("picoCTF{.+}", stdout_data).group(0))
