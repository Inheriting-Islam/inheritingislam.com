# Image brief — what to have ChatGPT make, and what it must never make

*For inheritingislam.com. Brand: deep pine `#183C34` · antique gold `#B08D57` · warm ivory
`#F5F0E6` · stone `#8C8F94` · sand `#DAD8D2`.*

---

## Read this first — the two hard limits

**1. No generated people. None.**
The entire argument of this site is that it was made by someone inside the community. An AI
photograph of "Muslims at a masjid" is the exact lie the site is built to be the opposite of, and
it is the one that will be spotted — by your own audience, who can tell. One synthetic face on
this site costs more trust than every image on it earns.

That rules out: worshippers, volunteers, students, teachers, hands holding a mushaf, a family at
iftar, a board meeting, anything that reads as documentary. Also rules out generated *places*
presented as real — a masjid interior, a specific city, a classroom.

**2. No generated Arabic, and no generated Qur'anic text. Ever.**
Image models cannot set Arabic. They produce letterforms that look like Arabic and are gibberish —
and on a page about teaching Qur'an, gibberish that resembles āyāt is not a design flaw, it is a
problem you will have to apologise for. Every Arabic character on this site is live text in Amiri,
which is correct and always will be.

If a prompt would put *any* lettering in the image, remove it. Type belongs to the site, not to
the picture.

**What is safe**, and what this brief is made of: **abstract, ornamental, and material.** Islamic
geometry, ink and paper textures, gold-leaf washes, colour fields, brand marks on physical
objects. None of it claims anything about the real world, so none of it can be a lie.

---

## Tier 1 — generate these (highest value first)

Save everything to `assets/img/`. Export PNG or JPG, then convert to `.webp` (there is a one-liner
at the end). Ask for **no text, no letters, no words** in every prompt — say it explicitly, models
add lettering unprompted.

### 1. Hero texture — the one that changes the most

*Where:* behind the home hero. *Size:* 2400 × 1400. *File:* `texture-girih.webp`

> A seamless, very low contrast Islamic girih pattern — an eight-point star strapwork lattice
> drawn as thin interlacing lines. Warm ivory background, hex #F5F0E6. Lines in a slightly
> darker warm tan, barely visible, like a blind emboss or a watermark on handmade paper.
> Extremely subtle — it should read as texture, not decoration. Flat vector, no shading, no
> gradients, no perspective, no drop shadows. No text, no letters, no words, no people.
> Wide 12:7 composition.

*Note:* if it comes back too strong, ask for "half the contrast" — you want it invisible until you
look for it. The CSS to drop it in is at the bottom of this file.

### 2. Podcast cover art — you need this anyway to submit the feed

*Where:* `/podcast/`, and Apple/Spotify. *Size:* **3000 × 3000** (platform requirement).
*File:* `podcast-cover.webp`

> A square podcast cover. Deep pine green background, hex #183C34. Centred: three interlocking
> diamond outlines forming a chain — the left and right links in warm ivory #F5F0E6, the middle
> link in antique gold #B08D57, woven so the gold passes under at the top and over at the bottom.
> Thick even strokes, sharp mitred corners, flat vector, no gradient, no bevel, no glow. Generous
> empty margin around the mark. No text, no letters, no words.

*Note:* the show title has to be legible at 55 px, so **set the title as live type over this in
Canva or Figma** — do not let the model draw it. I can also generate the finished cover with the
real fonts, the same way the share card in `assets/img/og-card.png` was made — say the word.

### 3–8. Six app tiles — this is what gives `/apps/` its colour

*Where:* the ledger rows on `/apps/`. *Size:* 800 × 800 each. *Files:* `app-itqan.webp`,
`app-jadhr.webp`, `app-sakinah.webp`, `app-noorreader.webp`, `app-asanid.webp`,
`app-sunrise.webp`

Use this shared preamble on all six so the set holds together:

> A square abstract app tile, flat vector, no text, no letters, no words, no people, no
> photorealism, no 3D, no gradients except where stated. Palette strictly: deep pine #183C34,
> antique gold #B08D57, warm ivory #F5F0E6, sand #DAD8D2. Centred symmetrical composition with
> generous margin. Then: …

…and finish each with:

| App | Ending |
|---|---|
| **Itqān** | *…a precise geometric lattice of nested squares tightening toward the centre, ivory lines on deep pine, suggesting mastery through repetition.* |
| **Jadhr** | *…three thick ink brush-like strokes radiating from a single point like a root system, gold on ivory, calm and playful.* |
| **Sakīnah** | *…a still horizontal band structure, wide calm rows in sand and ivory over pine, evoking balance and quiet.* |
| **NoorReader** | *…a single soft radial glow of gold light emerging from behind a flat ivory rectangle, like a page catching lamplight.* |
| **Asanīd** | *…a branching network of fine gold lines connecting small diamond nodes, spreading upward like a genealogy, on deep pine.* |
| **Sunrise Masjid** | *…a flat geometric horizon with a low gold semicircle sun behind simple stepped ivory silhouettes of rooftops — abstract shapes only, not a recognisable building.* |

*Note on Sunrise Masjid:* keep it abstract stepped forms. A mosque-with-dome-and-minaret
silhouette is on the site's banned list and would look like every other Muslim app on the store.

### 9. Founder-band paper texture

*Where:* behind the founder passage on the home page and `/about/`. *Size:* 2000 × 1200.
*File:* `texture-paper.webp`

> A flat scan of handmade cotton rag paper in warm ivory #F5F0E6. Visible fibre and a faint
> deckled grain, evenly lit, no shadows, no objects, no curl, no perspective. Neutral and
> uniform enough to place text over. No text, no letters, no words.

### 10. Section divider — the gold rule, as art

*Where:* between major bands, full-bleed. *Size:* 2400 × 300. *File:* `divider-chain.webp`

> A wide horizontal band, warm ivory #F5F0E6 background. A single row of small interlocking
> diamond outlines in antique gold #B08D57 running edge to edge like a chain, thin even strokes,
> flat vector, repeating and seamless left to right. Lots of empty space above and below. No
> text, no letters, no words.

---

## Tier 2 — photograph these yourself, do not generate them

These are the images that would actually move a masjid board, and they only work if they are real.
A phone in good daylight is enough.

- **Hamza.** One portrait, natural light, no studio look. The founder paragraph is the highest-
  converting block on the site and it currently has no face. This is the single biggest available
  upgrade, and it cannot be generated — it is the whole point.
- **Khadija**, if she is comfortable being pictured; if not, leave the space as it is.
- **The Al-Maun build in the world** — the site open on a phone, held, somewhere ordinary. Real
  screenshots are already on the site; a photograph of one in a hand adds warmth without adding a
  claim.
- **Your desk.** A photograph of where the work actually happens is truer than any
  illustration of it.
- **Al-Maun's own community photos** — they exist and they are strong, but they are the client's.
  Ask before publishing any of them here, in writing, and caption them as theirs.

---

## Tier 3 — probably skip

- Generated "masjid interior" hero images. Every Muslim org site has one; yours is better without.
- Illustrated people, flat-vector characters, "diverse team" illustrations. Same lie, softer edges.
- Anything with a crescent, a lantern, a dome silhouette, or an emerald-to-gold gradient — all
  four are on the design brief's automatic-fail list.

---

## Specs and how to install

**Format.** Ask for PNG, then convert — WebP is 60–80% smaller at the same quality:

```bash
cd ~/inheritingislam-com/assets/img
python3 -c "
from PIL import Image; import sys, glob
for f in glob.glob('*.png'):
    im = Image.open(f).convert('RGB')
    im.save(f.replace('.png','.webp'), 'WEBP', quality=82, method=6)
"
```

**Budget.** Keep each tile under 60 KB and each texture under 120 KB. Total page weight is a
design constraint on this site, not an afterthought — the whole thing is currently around 700 KB
including all nine pages' fonts.

**Textures** go in as CSS backgrounds, not `<img>` — they are decoration, so they should not be
announced to a screen reader:

```css
.hero{
  background-image:url('/assets/img/texture-girih.webp');
  background-size:cover; background-position:center;
}
:root[data-theme="dark"] .hero{ opacity:.35; }   /* textures need dulling in dark */
```

**App tiles** go in as real images with real alt text, inside each `.lrow` on `/apps/`. Send them
over and I will wire them in and re-run the render sweep.

**Already done for you:** `assets/img/og-card.png` — the link-preview card every page now points
at, drawn from the brand mark and the real fonts rather than generated. Paste any page URL into
WhatsApp or iMessage and that is what appears.
