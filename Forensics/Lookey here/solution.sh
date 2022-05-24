#!/bin/bash

../../utils/download_artifacts.sh

grep -Eo 'picoCTF\{.+\}' anthem.flag.txt
