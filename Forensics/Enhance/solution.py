#!/usr/bin/env python3
import lxml.etree

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

print("".join(
    lxml.etree.parse("drawing.flag.svg")
        .xpath(
        "//svg:text/svg:tspan/text()",
        namespaces={"svg": "http://www.w3.org/2000/svg"}
    )
).replace(" ", ""))
