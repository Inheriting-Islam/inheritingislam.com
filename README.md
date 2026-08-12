# inheritingislam.com

The house site for **Inheriting Islam** — the Studio, the Apps, Inheriting Qur'an, and the Podcast.

Static HTML. No framework, no build step, no backend, and no third-party requests of any kind.
Seventeen pages, about 2.3 MB in total including every image and both webfont families.

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
studio/                     The Studio — the problem, scope, process, ownership, pricing, FAQ
studio/care/                Care plans — the tiers, minor vs major, the seasons
studio/almaun/              Case study — Al-Maun Neighborly Needs
apps/                       Six apps, each with its real status
quran/                      Inheriting Qur'an — the program, $50/mo, the enrolment form
quran/start/                Placement check — five lines of Arabic, easiest first
quran/lesson/               Lesson one in full — letters, shapes, vowels, the five makhārij
quran/cohorts/              How a cohort runs, the schedule, the waitlist
quran/masajid/              Hosting a cohort + a one-page PDF for a board
quran/teacher/              Who teaches it, what the program is not, endorsements (empty)
quran/verify/               The certificate register — noindex, empty until the first cohort
podcast/                    Season one, in production — plus the episode index
podcast/guests/             Be a guest, or recommend the person who should be
about/                      Hamza, Khadija, the mīrāth thesis, the five rules
contact/                    Start a project — intake form (mailto) + direct contact
404.html

assets/css/fonts.css        Cormorant Garamond, Source Sans 3, Amiri — base64 woff2, one
                            cached request for the whole site (285 KB)
assets/css/site.css         The entire design system: tokens, both themes, every component
assets/css/quran.css        The Qur'an arm's skin: warmer bands, its own components
assets/css/studio.css       The Studio arm: the care ladder and the case-study metrics
assets/css/podcast.css      The Podcast arm: episode cards, transcripts, the feed switch
assets/js/site.js           Theme, nav, reveal, mailto composer, clipboard (~4 KB)
assets/js/quran.js          Placement check, letter panel, time zone, level hand-off (~7 KB)
assets/img/                 Hero artwork, app tiles, Al-Maun screenshots, share card, icons

docs/image-brief.md         What artwork to commission, and the two things never to generate
tools/check.py              The structural audit (also runs in CI)
tools/render-audit.py       Browser sweep: overflow at every breakpoint, both themes
tools/build-fonts.py        Rebuilds fonts.css from Google Fonts, subset to what we use
tools/build-onepager.py     Renders both leave-behind PDFs; fails if either spills past one page
tools/build-certificates.py Blank specimens for the site, or real PDFs from a CSV of graduates
tools/certificate.html      One template, three variants, driven by query parameters
tools/episode-template/     Copy this folder to podcast/<guest-slug>/ to publish an episode

_internal/NOTES.md          Delivery notes — read before publishing
_internal/NOTES-QURAN.md    Delivery notes for the Qur'an section
_internal/NOTES-STUDIO.md   Delivery notes for the Studio section
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
Change one, change all fourteen. `aria-current="page"` marks the active nav item.

**Arm sections.** `/quran/` and `/studio/` each have enough pages to need local navigation, so
they carry `data-arm="…"` on `<body>` and a second sticky `.armbar` under the header (folded into
the mobile panel below 1000px), and their footer's third column lists the arm's own pages. The
Qur'an pages also swap the header's primary button to **Join a class**, because a student arriving
to learn to read should not be sold a website build. The shared chrome lives in `site.css` under
"ARM SECTIONS"; each arm's stylesheet holds only what is particular to it — and `studio.css` shifts
no colour token at all, because the Studio is the house's default register.

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
