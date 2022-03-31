#!/bin/bash

../../utils/download_artifacts.sh

chmod +x run
./run | awk '{ print $NF }'
