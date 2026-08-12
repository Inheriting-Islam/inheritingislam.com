#!/usr/bin/env python3
"""Render the leave-behind one-pagers to PDF.

    python3 -m http.server 8080          # in one terminal, from the repo root
    python3 tools/build-onepager.py      # in another — renders every sheet
    python3 tools/build-onepager.py --only board

Each sheet is a single Letter page a person can print and hand to a board.
Sources live in tools/ rather than _internal/ so a fresh clone can rebuild them
(_internal/ is gitignored); check.py skips tools/, so they are never audited as
site pages.

Served over HTTP rather than opened from file:// so that the base64 webfonts in
assets/css/fonts.css load — a file:// render silently falls back to Helvetica
and the sheet stops looking like the site.
"""
import os, re, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# name → (source under tools/, output path in the site)
SHEETS = {
    "masajid": ("onepager-masajid.html",
                "quran/masajid/inheriting-quran-for-masajid.pdf"),
    "board":   ("onepager-board.html",
                "studio/inheriting-islam-for-your-board.pdf"),
}

args = [a for a in sys.argv[1:]]
only = None
if "--only" in args:
    i = args.index("--only")
    only = args[i + 1]
    del args[i:i + 2]
    if only not in SHEETS:
        sys.exit(f"Unknown sheet {only!r}. Choose from: {', '.join(SHEETS)}")
BASE = args[0] if args else "http://localhost:8080"

if not os.path.exists(CHROME):
    sys.exit(f"Chrome not found at {CHROME}")
try:
    urllib.request.urlopen(BASE, timeout=4)
except Exception:
    sys.exit(f"Nothing serving {BASE} — run: python3 -m http.server 8080")

failures = []
for name, (src, out_rel) in SHEETS.items():
    if only and name != only:
        continue
    out = os.path.join(ROOT, out_rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={out}",
        f"{BASE}/tools/{src}",
    ], check=True, capture_output=True)

    raw = open(out, "rb").read()
    pages = len(re.findall(rb"/Type\s*/Page[^s]", raw))
    print(f"{out_rel} · {len(raw)/1024:.0f} KB · {pages} page(s)")

    # These are one-pagers. Two pages means the content grew and the sheet
    # silently split — a fail, not a warning, because nobody notices page two.
    if pages != 1:
        failures.append(f"{name}: expected 1 page, produced {pages}. Trim tools/{src}.")
    if len(raw) < 20_000:
        failures.append(f"{name}: suspiciously small — the webfonts did not embed.")

if failures:
    sys.exit("FAIL  " + "\n      ".join(failures))
