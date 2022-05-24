#!/usr/bin/env python3

import json
import re
import subprocess
import r2pipe
import os
import stat

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

binary_name = "bbbbloat"
r = r2pipe.open(binary_name, flags=["-node", "bin.cache=true"])
r.cmd("aaa")


def r_cmd_json(cmd, args):
    return json.loads(r.cmd(f"{cmd}j {args}"))


message_data = r_cmd_json("/", "Sorry, that's not it!")[0]["offset"]
jump_target = r_cmd_json("axt", message_data)[0]["from"]
jump = r_cmd_json("axt", jump_target)[0]["from"]
r.cmd(f"s {jump}")
cmp_value = r_cmd_json("pdj", -1)[0]["val"]

binary_path = f"./{binary_name}"
st = os.stat(binary_path)
os.chmod(binary_path, st.st_mode | stat.S_IEXEC)

p = subprocess.Popen([binary_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
stdout = p.communicate(str(cmp_value).encode())[0].decode()
print(re.search("picoCTF{.+}", stdout).group(0))
