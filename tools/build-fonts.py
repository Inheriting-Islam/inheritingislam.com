#!/usr/bin/env python3
"""Fetch full TTFs from Google Fonts, subset to the charset this site actually needs,
compress to woff2, and emit one base64 data-URI @font-face stylesheet.

Why not the stock Google 'latin' subset? It omits U+012B (ī), U+0101 (ā), U+016B (ū) —
i.e. every long vowel in mīrāth, Itqān, Sakīnah, tajwīd, Qur'ān. Those would fall back
to a system font mid-word. We subset ourselves so the diacritics belong to the face.
"""
import urllib.request, re, os, base64, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'ttf'); os.makedirs(RAW, exist_ok=True)
OUT = os.path.join(HERE, 'woff2'); os.makedirs(OUT, exist_ok=True)
PYFT = os.path.join(HERE, 'fx', 'bin', 'pyftsubset')
OLD_UA = {'User-Agent': 'Mozilla/4.0'}          # -> ttf urls (full charset)

# --- charset -------------------------------------------------------------
LATIN = ",".join([
    "U+0020-007E",            # basic latin
    "U+00A0-00FF",            # latin-1 supplement (©, ·, é, ñ, ×, …)
    "U+0100-017F",            # latin extended-A  (ā ī ū ġ ...)
    "U+02BB-02BC", "U+02BE-02BF",   # ʻ ʼ  ʾ ʿ  (hamza / ayn)
    "U+0304", "U+0331",       # combining macron above/below
    "U+1E0C-1E0D", "U+1E24-1E25", "U+1E62-1E63", "U+1E6C-1E6D", "U+1E92-1E93",  # Ḍḍ Ḥḥ Ṣṣ Ṭṭ Ẓẓ
    "U+2010-2015", "U+2018-201E", "U+2020-2022", "U+2026", "U+2030",
    "U+2032-2033", "U+2039-203A", "U+2044", "U+2052",
    "U+20AC", "U+2122", "U+2190-2193", "U+2212", "U+2215", "U+2713",
])
ARABIC = ",".join([
    "U+0020-007E", "U+00A0",
    "U+060C", "U+061B", "U+061F",       # ، ؛ ؟
    "U+0621-063A", "U+0640-064A",       # letters + tatweel
    "U+064B-0655", "U+0670",            # harakat, dagger alif
    "U+0660-0669", "U+066A-066D",
    "U+06D6-06DC", "U+06DD-06ED",       # qur'anic marks
    "U+FD3E-FD3F",
])

# slug, css family name, css2 query, subset charset, faces we keep
JOBS = [
    ('cormorant', 'Cormorant Garamond',
     'family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400', LATIN),
    ('sourcesans', 'Source Sans 3', 'family=Source+Sans+3:wght@400;600;700', LATIN),
    ('amiri', 'Amiri', 'family=Amiri:wght@400', ARABIC),
]

FACE = re.compile(r'@font-face\s*\{(.*?)\}', re.S)

def get(url, headers=OLD_UA):
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60).read()

faces = []
for slug, family, query, charset in JOBS:
    css = get(f'https://fonts.googleapis.com/css2?{query}&display=swap').decode()
    seen = set()
    for m in FACE.finditer(css):
        b = m.group(1)
        style = 'italic' if re.search(r'font-style:\s*italic', b) else 'normal'
        wt = re.search(r'font-weight:\s*(\d+)', b)
        wt = wt.group(1) if wt else '400'
        u = re.search(r'url\((https://[^)]+\.(?:ttf|woff2))\)', b)
        if not u or (style, wt) in seen:
            continue
        seen.add((style, wt))
        ttf = os.path.join(RAW, f'{slug}-{style[0]}{wt}.ttf')
        if not os.path.exists(ttf):
            open(ttf, 'wb').write(get(u.group(1)))
        w2 = os.path.join(OUT, f'{slug}-{style[0]}{wt}.woff2')
        subprocess.run([PYFT, ttf, f'--unicodes={charset}', '--flavor=woff2',
                        '--layout-features=*', '--no-hinting', '--desubroutinize',
                        f'--output-file={w2}'], check=True)
        faces.append((family, style, wt, w2, os.path.getsize(ttf), os.path.getsize(w2)))
        print(f'{family:12} {style:7} {wt}   {os.path.getsize(ttf)//1024:>5} KB ttf  ->  {os.path.getsize(w2)//1024:>4} KB woff2')

out = ["/* Inheriting Islam — type. Subset from the full faces so the long vowels (ā ī ū)",
       "   and the Arabic belong to the family, not to a fallback. Self-hosted as data URIs:",
       "   one cached request for the whole site, zero third-party connections. */"]
for family, style, wt, path, _, _ in faces:
    b64 = base64.b64encode(open(path, 'rb').read()).decode()
    out.append(f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{wt};"
               f"font-display:swap;src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
css = "\n".join(out) + "\n"
dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'fonts.css')
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, 'w').write(css)
print(f"\nwrote {dest}: {len(css)//1024} KB  ({len(faces)} faces, "
      f"{sum(f[5] for f in faces)//1024} KB of woff2)")
