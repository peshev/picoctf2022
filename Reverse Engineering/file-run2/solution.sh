#!/bin/bash

../../utils/download_artifacts.sh

chmod +x run
./run 'Hello!' | awk '{ print $NF }'
