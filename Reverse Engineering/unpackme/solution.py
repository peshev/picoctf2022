#!/usr/bin/env python3

import json
import os
import re
import subprocess
import r2pipe

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

binary_name = "unpackme-upx"
unpacked_binary_name = binary_name + ".unpacked"

os.chmod(binary_name, 0o755)

if os.path.exists(unpacked_binary_name):
    os.unlink(unpacked_binary_name)

subprocess.check_output(["upx", "-d", binary_name, "-o", unpacked_binary_name])

r = r2pipe.open(unpacked_binary_name, flags=["-node", "bin.cache=true"])
r.cmd("aaa")


def r_cmd_json(cmd, args):
    return json.loads(r.cmd(f"{cmd}j {args}"))


message_data = r_cmd_json("/", "Sorry, that's not it!")[0]["offset"]
jump_target = r_cmd_json("axt", message_data)[0]["from"]
jump = r_cmd_json("axt", jump_target)[0]["from"]
r.cmd(f"s {jump}")
cmp_value = r_cmd_json("pdj", -1)[0]["val"]

p = subprocess.Popen([f"./{binary_name}"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)
output = p.communicate(str(cmp_value).encode())[0].decode()
print(re.search("picoCTF{.+}", output).group(0))
