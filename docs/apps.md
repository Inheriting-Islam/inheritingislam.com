# The apps — what each one actually is

*Source of truth for the statuses on `/apps/`. Compiled 2026-08-11 by reading every repository
rather than trusting an earlier summary — which had four of the seven wrong.*

*Updated 2026-10-07: Life Is Temporary added as the first live app, and **Live** added as a fifth
defined word.*

Status vocabulary, as defined on the page itself:
**Live** — public and working; anyone can use it today, and we keep it maintained.
**In development** — real code exists and is being worked on, not installable by you yet.
**Private beta** — working software in the hands of a small number of people who know they are early.
**Concept** — a designed, thought-through idea with nothing built.
**Set down** — real code that runs, with nobody working on it now and every intention of coming back.

| App | Status | Evidence |
|---|---|---|
| Life Is Temporary | Live | lifeistemporary.com · public, free · repo `Inheriting-Islam/lifeistemporary` |
| Itqān | In development | 164 commits · TypeScript · unit + Playwright e2e suites |
| Jadhr | In development | Playable prototype + the content engine behind it |
| Sakīnah | Private beta | 30 commits · client + server + Prisma · in daily personal use |
| NoorReader | In development | Swift 6 · macOS and iOS targets · four phased build specs |
| Sunrise Masjid | In development | 69 commits · Godot · **v0.1.0 vertical slice, code-complete** |
| Saif al-Ummah | In development | ~25,600 lines across 31 modules · playable · roadmap to 1.0 |
| Asanīd | Concept | Build plan and licence only — no code, by design |

---

## Life Is Temporary

Free guidance for Muslim families when someone dies, and for preparing ahead: step-by-step guides
for the US, UK and Canada, a directory of Muslim funeral services in six countries, an inheritance
calculator for all four schools, and a will draft builder. Live at
[lifeistemporary.com](https://lifeistemporary.com/).

**The story.** It is the first of the house's apps that anyone can open today, which is why `/apps/`
needed a fifth word. No Arabic name is shown on the page until one is confirmed.

## Itqān — إتقان · *mastery, doing a work with excellence*

A local-first, mastery-based path through the Islamic sciences, starting with Qur'anic Arabic:
recognition, production with full tashkīl, word-by-word iʿrāb parsing, rule citation and exceptions
across the Madinah Books, scheduled with FSRS-6. Real āyāt as the examples. The lesson model is
deliberately subject-agnostic so tajwīd, fiqh and ḥadīth can follow.

**The story.** No accounts, no cloud, no telemetry — your entire study history is one SQLite file
you can back up yourself. That is a position, not an architecture choice: a student's record of
what they know is not a thing to be hosted and monetised. It is the most built of the seven,
and the one designed to eventually earn.

## Jadhr — جذر

A daily Arabic habit. One minute. Built to be passed between people.

**Deliberately not described further** — the idea is the whole product and it is not shipped yet.
There is a working prototype and a content engine behind it. That is all the page says, and all
this file says.

## Sakīnah — سكينة · *tranquillity*

A private halal personal-finance tracker: income and expenses, four savings buckets, goals,
recurring rules, zakat, FBAR alerting, CSV export.

**The story.** It was built because the alternative was handing a full picture of your money to a
company whose business is knowing it. Everything stays on your own machine. It is the only one of
the seven in real daily use — which is what makes it a private beta rather than a plan.

## NoorReader — نور · *light*

A serious PDF and EPUB reader for macOS and iOS, built for studying Islamic texts: semantic
highlight colours, notes attached to highlights, keyboard-first navigation, day/sepia/night, and
reminders woven into the reading rather than bolted on as notifications.

**The story.** Its own README opens with the principle that seeking knowledge is an act of worship,
and asks for the work to be built with iḥsān. It is a reading app for people who read the way
students of knowledge read.

## Sunrise Masjid *(working title)*

A 2.5D platformer about Muslim life — African American, West African, and the wider ummah. The
vertical slice is *South Central Sunrise*: a walk to the masjid at Fajr in South Los Angeles, plus
a three-phase **Waswas** boss arena.

**The story.** Our children play games that never once look like them. This one is set in a
neighbourhood that does. Built to first-party game-feel standards, and deliberately gated: it does
not go out until the consultation sign-offs are in. The name is a working title.

**This is not a concept.** It is a code-complete v0.1.0 internal build.

## Saif al-Ummah — سيف الأمة · *the sword of the ummah*

An Islamic action-RPG: exploration across large tiled regions, both turn-based and realtime combat,
story moments, ambience, an autotiling world engine. Roughly 25,600 lines across 31 modules.

**The story.** Its roadmap opens with an unusually honest line — that the Islamic content and
systems design are best-in-class while the presentation does not yet match the ambition — and then
lists exactly what would close the gap: hit-feel and game juice, a named antagonist with a real
motive rather than a stat block, filling the empty space between landmarks, pixel art in place of
placeholder icons. That is a builder who knows precisely where his own work stands.

**Risk, urgent.** It has **no git history and no remote**. It lives in `~/saif-al-ummah` and
nowhere else. Jadhr's README already records losing a scratchpad and having to recover the work
from local file history. Put this one in a private repo today.

## Asanīd — أسانيد · *chains of transmission*

Three pillars on one knowledge graph: **Chains** (every scholar, ijāza and silsila mapped across
regions, madhāhib and centuries), **Madāris** (every madrasah, hifz school and academy as a
verified structured page), and **Riḥla** (a personal journey tracker, so today's student becomes
tomorrow's node). A tiered verification model keeps paid listings walled off from verified
scholarship, so directory revenue can subsidise the heritage work without corrupting it.

**The story.** The stated edge is reach — Senegal and the Tijāniyya, Morocco and Maghribī Mālikī,
Turkey and Ottoman Ḥanafī, Black American Sunni heritage — the regions every "global Muslim
platform" underserves.

**Genuinely a concept**, and correctly so: a thorough build plan and no code. It needs scholarly
partners before it needs a repository.
