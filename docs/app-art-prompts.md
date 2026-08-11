# App artwork — prompts

*Seven images, one per app. These replace the flat geometric tiles, which said "brand" rather than
"product". Each one should look like the thing it is.*

## Two families, on purpose

**The five tools** — Itqān, Jadhr, Sakīnah, NoorReader, Asanīd — are **photographic still lifes**,
in the same visual language as the site's hero images: real materials, warm directional light, deep
pine shadow, antique gold, shallow depth of field. They sit beside those heroes, so they should
look like they were shot on the same afternoon.

**The two games** — Sunrise Masjid and Saif al-Ummah — are **key art in their own idiom**. A
photograph of a game misrepresents it. Sunrise Masjid is illustrated 2.5D; Saif al-Ummah is
painterly pixel-art RPG. Their tiles should look like a frame you could play.

## Two rules that carry over

**No readable writing.** Where a book or page appears, instruct that any script be soft-focused and
illegible. Image models cannot set Arabic — they produce letterforms that look right and say
nothing — and garbled script on a page about the Islamic sciences is not a small error.

**No faces.** Distant or silhouetted figures are fine in the game art, where nobody could mistake
an illustration for a documentary photograph. Everywhere else, no people.

## Format

Square, 1024 × 1024, PNG → convert to `.webp` at quality 86 (`tools/`, or the one-liner in
`image-brief.md`). File names: `app-itqan.webp`, `app-jadhr.webp`, `app-sakinah.webp`,
`app-noorreader.webp`, `app-sunrise.webp`, `app-saif.webp`, `app-asanid.webp`.

> **These deserve more room than they currently get.** The apps ledger shows them at 60 px, which
> wastes real artwork. Worth moving `/apps/` to a card layout with the art at a proper size — ask
> and I will rebuild it.

---

## 1 · Itqān — the mastery path

> A warm, photographic still life on a wooden study desk: an open grammar workbook with a second
> book stacked beside it, a neat fan of handwritten study cards, a fountain pen resting on a
> notebook, and a small brass lamp casting warm directional light from the left. Deep pine green
> shadows, antique gold highlights, warm ivory paper. Any writing on the pages must be softly out
> of focus and illegible — do not attempt to render readable script. Shallow depth of field, real
> paper grain and wood texture, unhurried and scholarly. No people, no hands, no legible text.
> Square composition.

## 2 · Jadhr — the one we do not explain

> A quiet, photographic still life: a single reed qalam resting across a sheet of unbleached
> handmade paper, beside a small closed inkwell, on a dark wooden surface. One small stroke of dark
> ink on the paper, nothing more. Low warm light from one side, deep shadow, generous empty space.
> The mood is anticipation — something about to begin. No people, no hands, no text, no letters.
> Square composition.

*It should invite a question and answer none of it. Nothing in this frame explains the game.*

## 3 · Sakīnah — private, halal money

> A calm photographic still life: a small brass balance scale in perfect equilibrium on a dark
> wooden table, beside a closed leather ledger and a shallow dish holding a few coins. Warm side
> light, deep pine green background falling into shadow, antique gold on the brass. Everything
> level, ordered, and still — the feeling is tranquillity and control, not wealth. No people, no
> hands, no text, no logos, no currency symbols. Shallow depth of field. Square composition.

## 4 · NoorReader — study, lit from within

> A photographic still life at night: an open book lying flat on a desk with a scattering of small
> coloured tabs marking its pages, a pair of reading glasses folded beside it, and a warm lamp just
> out of frame throwing a pool of gold light across the paper. The room beyond falls into deep pine
> darkness. The page text must be soft-focused and illegible. Warm ivory paper, antique gold light,
> real texture. No people, no hands, no legible text, no screens. Square composition.

## 5 · Asanīd — the chains, mapped

> A photographic still life in an old library: three or four aged manuscripts stacked and fanned on
> a dark wooden table, with a fine chain of small brass links resting across them and trailing off
> the edge of the frame. Warm directional light, deep shadow behind, antique gold on the brass,
> aged paper in warm ivory. Any script on the manuscripts must be soft-focused and illegible. The
> feeling is lineage and custody — things handed down intact. No people, no hands, no legible text.
> Square composition.

## 6 · Sunrise Masjid — game key art

> Illustrated 2.5D video-game key art, not a photograph. A South Los Angeles residential street at
> dawn: low houses, chain-link fences, power lines, palm trees in silhouette, and the modest
> minaret of a neighbourhood masjid a few blocks ahead. The sun is just breaking the horizon in
> warm gold behind it. A single small figure, seen from behind and far away as a silhouette, walks
> up the middle of the street toward the masjid. Rich painterly game-art style with clean readable
> shapes and strong depth layering — foreground, midground, sky. Deep pine and indigo shadow, warm
> gold light. Nobody's face is visible. No text, no letters, no UI or interface elements. Square
> composition.

## 7 · Saif al-Ummah — game key art

> Painterly pixel-art key art for an action-RPG, not a photograph. A wide arid landscape at dusk:
> a curved sword planted upright in the ground in the near foreground, a worn road winding away
> behind it, and the silhouette of a walled fortress city on the far horizon under a deep sky. Warm
> gold light on the blade and the horizon, deep pine and indigo in the shadows and sky. Detailed
> pixel art with a limited palette and strong readable silhouettes, in the register of a serious
> 16-bit RPG rather than a cartoon. No people, no text, no letters, no UI or interface elements.
> Square composition.

---

## If a result comes back wrong

Two failure modes, both common. **Invented script** — a model will add letterforms to a page even
when told not to; discard those, they are gibberish and worse than blank. **Too clean** — if it
looks like a stock render, ask for "real material wear, dust, uneven light, imperfect placement."
Generate four of each and take the one that looks like it belongs in a room rather than a catalogue.
