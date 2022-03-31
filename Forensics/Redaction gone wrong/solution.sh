#!/bin/bash

../../utils/download_artifacts.sh

pdftotext Financial_Report_for_ABC_Labs.pdf - | grep pico
