#!/bin/bash

../../utils/download_artifacts.sh

decrypt_command=$(tshark -r capture.flag.pcap -z follow,tcp,raw,0 | sed -n '/===/,/===/p' | head -n -1 | tail -n +6 | sed -n 4p | xxd -r -p | cut -d\  -f2-)
tshark -r capture.flag.pcap -z follow,tcp,raw,2 | sed -n '/===/,/===/p' | head -n -1 | tail -n +6 | xxd -r -p > file.des3
$($decrypt_command 2> /dev/null)
cat file.txt
echo