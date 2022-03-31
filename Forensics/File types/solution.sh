#!/bin/bash

../../utils/download_artifacts.sh

rm flag 2> /dev/null
chmod +x Flag.pdf
./Flag.pdf > /dev/null
ar -x flag
cat flag | cpio -i --to-stdout 2> /dev/null | bunzip2 | gunzip | lzip -d | lz4cat | lzmadec | lzop -d | lzip -d | xzcat | xxd -r -p
