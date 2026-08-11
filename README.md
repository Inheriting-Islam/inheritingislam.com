# inheritingislam.com

The house site for **Inheriting Islam** — the Studio, the Apps, Inheriting Qur'an, and the Podcast.

Static HTML. No framework, no build step, no backend, and no third-party requests of any kind.
Nine pages, about 2 MB in total including every image and both webfont families.

**Deploying it for the first time? → [`DEPLOY.md`](DEPLOY.md).** That is the build plan: four
gates, starting with the claims on the site that only Hamza can confirm.

---

## Run it locally

Pages reference assets with root-absolute paths, so serve the folder — do not open the files
from Finder:

```bash
python3 -m http.server 8080
# → http://localhost:8080
```

## Check it

```bash
python3 tools/check.py
```

Links and anchors, one `<h1>` per page, landmarks, alt text, form labels, `lang="ar"` on every
Arabic string, third-party requests, and phrases that would overclaim. No browser needed, runs in
under a second, and runs again in CI on every push.

For layout and colour changes, the browser sweep — renders every page at 1440px and 390px in both
themes and fails on horizontal overflow:

```bash
python3 tools/render-audit.py http://localhost:8080 "/,/studio/,/apps/,/quran/"
```

## What is where

```
index.html                  Home — thesis, four arms, Al-Maun, pricing, the founder
studio/                     The Studio — context, scope, process, pricing, MasjidBuilder
studio/almaun/              Case study — Al-Maun Neighborly Needs
apps/                       Six apps, each with its real status
quran/                      Inheriting Qur'an — the program, $50/mo, hosting a cohort
podcast/                    Season one, in production
about/                      Hamza, Khadija, the mīrāth thesis, the five rules
contact/                    Start a project — intake form (mailto) + direct contact
404.html

assets/css/fonts.css        Cormorant Garamond, Source Sans 3, Amiri — base64 woff2, one
                            cached request for the whole site (285 KB)
assets/css/site.css         The entire design system: tokens, both themes, every component
assets/js/site.js           Theme, nav, reveal, mailto composer, clipboard (~4 KB)
assets/img/                 Hero artwork, app tiles, Al-Maun screenshots, share card, icons

docs/image-brief.md         What artwork to commission, and the two things never to generate
tools/check.py              The structural audit (also runs in CI)
tools/render-audit.py       Browser sweep: overflow at every breakpoint, both themes
tools/build-fonts.py        Rebuilds fonts.css from Google Fonts, subset to what we use
```

## The design

**"Atelier."** Dark first — the default surface is pine-black and the light theme is a parchment
gallery, both deliberately designed rather than one inverted into the other. Hero artwork runs
full-bleed to the right edge at full strength while the type sits on solid ground beside it;
**text is never set over the photograph**, because scrimming an image enough to read type ruins
the image. Typography is the brand sheet's own — Cormorant Garamond for display, Source Sans 3 for
everything functional, Amiri for Arabic.

Colours and type live entirely in the `:root` blocks at the top of `assets/css/site.css`. Nothing
else in the codebase hardcodes a colour. Both themes are written as attribute selectors so neither
can win on specificity by accident.

## Editing

**Copy** is plain HTML — edit in place.

**Header, footer and nav** are repeated in every page deliberately, since there is no build step.
Change one, change all nine. `aria-current="page"` marks the active nav item.

**Status pills** — `<span class="pill live|dev|beta|concept">…</span>`. Those four words are
defined on `/apps/`; keep them meaning exactly what that page says they mean.

**Fonts** are subset to Latin plus the diacritics the copy actually needs (ā ī ū ʿ ḥ ṣ …) and the
Arabic block. Google's stock `latin` subset omits U+012B (ī), which would drop every long vowel in
*mīrāth*, *Itqān* and *tajwīd* to a fallback font mid-word — hence `tools/build-fonts.py`.

## Themes

Respects `prefers-color-scheme`, remembers a manual choice in `localStorage` (`ii-theme`), and
accepts `?theme=dark` / `?theme=light` for sharing a specific view. A boot script in each `<head>`
sets the attribute before first paint, so there is no flash.

## The contact form

No backend. The form composes a complete `mailto:` to `hamza@inheritingislam.com` and hands it to
the visitor's own mail app — so nothing sits between their address and ours, and they can see
exactly what is being sent. To swap in a real endpoint later, replace the submit handler in
`assets/js/site.js`; the field names are already sensible.

## What this site holds itself to

- **Zero third-party requests.** No CDN, no fonts API, no analytics, no cookies. The only
  non-relative link on the whole site is to `itqan.inheritingislam.com`. Enforced by CI.
- **WCAG AA.** 4.5:1 or better on every piece of text in both themes — computed, not eyeballed,
  including the backdrop behind the hero type at five viewport sizes.
- **No horizontal overflow** at 390px, verified page by page in both themes.
- **Honest status.** Nothing here describes work as finished that is not finished. That includes
  our own flagship case study, and it is the reason the rest of the site is worth believing.
