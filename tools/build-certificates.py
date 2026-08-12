#!/usr/bin/env python3
"""Render the graduation certificates.

    python3 -m http.server 8080            # in one terminal, from the repo root
    python3 tools/build-certificates.py    # blank specimens for the site
    python3 tools/build-certificates.py --issue graduates.csv

Two modes, and the difference matters:

  SPECIMENS (default) — the three certificates rendered BLANK, as images only,
  into assets/img/. These are what the site shows. There is no name on them and
  no PDF published, so there is nothing for anyone to edit: a forger would have
  to add a name, which the verification number then fails to match.

  ISSUE — real certificates for real graduates, as print-ready PDFs written to
  _issued/ (gitignored, never published). One row per graduate:

      name,name_ar,gender,type,id,hijri,gregorian
      Aisha Karim,عائشة كريم,f,qaidah,IQ-Q-1448-014,15 Ramaḍān 1448,15 March 2027

  gender is m or f and decides the Arabic verb agreement — a certificate that
  gets a woman's grammar wrong is worse than no certificate.
  type is qaidah, tajwid or hifz.

Served over HTTP rather than file:// so the base64 webfonts in
assets/css/fonts.css load; a file:// render silently falls back to Helvetica
and the Arabic falls back to something that is not Amiri.
"""
import csv, os, re, subprocess, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TYPES = ("qaidah", "tajwid", "hifz")

args = sys.argv[1:]
issue_csv = None
if "--issue" in args:
    i = args.index("--issue")
    issue_csv = args[i + 1]
    del args[i:i + 2]
BASE = args[0] if args else "http://localhost:8080"

if not os.path.exists(CHROME):
    sys.exit(f"Chrome not found at {CHROME}")
try:
    urllib.request.urlopen(BASE, timeout=4)
except Exception:
    sys.exit(f"Nothing serving {BASE} — run: python3 -m http.server 8080")


def url(**params):
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    return f"{BASE}/tools/certificate.html?{q}"


def to_pdf(src, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", "--virtual-time-budget=8000",
        f"--print-to-pdf={out}", src,
    ], check=True, capture_output=True)
    raw = open(out, "rb").read()
    pages = len(re.findall(rb"/Type\s*/Page[^s]", raw))
    if pages != 1:
        sys.exit(f"FAIL  {os.path.basename(out)} produced {pages} pages, expected 1.")
    if len(raw) < 20_000:
        sys.exit(f"FAIL  {os.path.basename(out)} is suspiciously small — webfonts did not embed.")
    return len(raw)


# Letter landscape at 96dpi — the sheet's exact size in CSS pixels.
SHEET_W, SHEET_H = 1056, 816


def to_image(src, out, width=1400):
    """A site image: big enough to admire, too small to print convincingly.

    The window must match the sheet exactly and the scale factor do the
    enlarging — a larger window just renders the sheet at its fixed size on a
    field of background, which crops wrong.
    """
    scale = round(width / SHEET_W, 4)
    tmp = out + ".png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        f"--window-size={SHEET_W},{SHEET_H}",
        "--hide-scrollbars", "--virtual-time-budget=8000",
        f"--force-device-scale-factor={scale}",
        f"--screenshot={tmp}", src,
    ], check=True, capture_output=True)
    from PIL import Image
    im = Image.open(tmp).convert("RGB")
    im.save(out, "WEBP", quality=88, method=6)
    os.remove(tmp)
    return os.path.getsize(out)


if issue_csv:
    rows = list(csv.DictReader(open(issue_csv, encoding="utf-8")))
    if not rows:
        sys.exit(f"{issue_csv} has no rows.")
    seen = set()
    for r in rows:
        cid = (r.get("id") or "").strip()
        if not cid:
            sys.exit(f"Every row needs an id. Missing for {r.get('name')!r}.")
        if cid in seen:
            sys.exit(f"Duplicate certificate id {cid!r} — every one must be unique.")
        seen.add(cid)
        if r.get("type") not in TYPES:
            sys.exit(f"{cid}: type must be one of {', '.join(TYPES)}, got {r.get('type')!r}.")
        out = os.path.join(ROOT, "_issued", f"{cid}.pdf")
        size = to_pdf(url(type=r["type"], name=r.get("name"), ar=r.get("name_ar"),
                          g=r.get("gender"), id=cid, hijri=r.get("hijri"),
                          greg=r.get("gregorian")), out)
        print(f"  _issued/{cid}.pdf · {size/1024:.0f} KB · {r.get('name')}")
    print(f"\n{len(rows)} issued. _issued/ is gitignored — these are never published.")
    print("Add each id to quran/verify/ before sending them out.")
else:
    for t in TYPES:
        out = os.path.join(ROOT, "assets", "img", f"cert-{t}.webp")
        size = to_image(url(type=t), out)
        print(f"  assets/img/cert-{t}.webp · {size/1024:.0f} KB · blank specimen")
    print("\nSpecimens are blank and image-only by design — nothing to edit, no PDF published.")
