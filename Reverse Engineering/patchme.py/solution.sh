#!/bin/bash

../../utils/download_artifacts.sh

patch < solution.diff > /dev/null
python patchme.flag.py
