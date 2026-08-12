#!/usr/bin/env python3
"""Render the masajid one-pager to PDF.

    python3 -m http.server 8080          # in one terminal, from the repo root
    python3 tools/build-onepager.py      # in another

Source  : tools/onepager-masajid.html
Output  : quran/masajid/inheriting-quran-for-masajid.pdf

Served over HTTP rather than opened from file:// so that the base64 webfonts in
assets/css/fonts.css load — a file:// render silently falls back to Helvetica
and the sheet stops looking like the site.
"""
import os, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
SRC = BASE + "/tools/onepager-masajid.html"
OUT = os.path.join(ROOT, "quran", "masajid", "inheriting-quran-for-masajid.pdf")

if not os.path.exists(CHROME):
    sys.exit(f"Chrome not found at {CHROME}")
try:
    urllib.request.urlopen(BASE, timeout=4)
except Exception:
    sys.exit(f"Nothing serving {BASE} — run: python3 -m http.server 8080")

subprocess.run([
    CHROME, "--headless", "--disable-gpu", "--no-sandbox",
    "--no-pdf-header-footer",
    "--virtual-time-budget=8000",
    f"--print-to-pdf={OUT}",
    SRC,
], check=True, capture_output=True)

import re

raw = open(OUT, 'rb').read()
pages = len(re.findall(rb'/Type\s*/Page[^s]', raw))
print(f"{os.path.relpath(OUT, ROOT)} · {len(raw)/1024:.0f} KB · {pages} page(s)")

# It is a one-pager. Two pages means the content grew and the sheet silently
# split — a fail, not a warning, because nobody notices page two.
if pages != 1:
    sys.exit(f"FAIL  expected 1 page, produced {pages}. Trim tools/onepager-masajid.html.")
if len(raw) < 20_000:
    sys.exit("FAIL  suspiciously small — the webfonts did not embed.")
