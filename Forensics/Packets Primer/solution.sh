#!/bin/bash

../../utils/download_artifacts.sh

tshark -r network-dump.flag.pcap -z follow,tcp,ascii,0 | sed 's/ //g' | grep picoCTF
