#!/usr/bin/env python3
"""
Entrypoint for the news-image-20261120 entry "Friday 20 November
2026: 38 stories, 7 regions \u2014 Kyiv bridges hit, Cyclone Akvan
landfall, AI sell-off sinks Asia, COP31 no deal".

The deliverable is one finished broadsheet page, entry.png, drawn
beforehand by draw.py (the build tool, kept in this repo) and
committed as an asset. This program's only job is to copy that asset
into the output directory the runner provides, byte for byte, using
nothing but the Python standard library.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(ASSET, dest)
    print("wrote %s (%d bytes)" % (dest, os.path.getsize(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
