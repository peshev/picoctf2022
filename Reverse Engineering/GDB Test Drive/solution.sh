#!/bin/bash

../../utils/download_artifacts.sh

chmod +x gdbme
gdb gdbme << EOF | grep picoCTF
break *(main+99)
run
jump *(main+104)
EOF


