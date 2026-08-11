# Build plan — getting this live on inheritingislam.com

*Four gates. Nothing moves to the next one until the current one is genuinely done, because
the whole argument of this site is that we do not claim things early.*

---

## Where it lives

| | |
|---|---|
| **Repo** | `Inheriting-Islam/inheritingislam.com` |
| **Host** | GitHub Pages, deployed by Actions from `main` |
| **Domain** | `inheritingislam.com` (apex) + `www` redirect |
| **Preview** | `https://inheriting-islam.github.io/inheritingislam.com/` — *paths break on a subpath, see below* |

The repo is **public** because GitHub Pages needs it to be on a free organisation plan. Every
other site repo in the org is public too, so this is consistent. Internal strategy notes are
deliberately **not** in this repo — see the last section.

> `assets/` is referenced with root-absolute paths (`/assets/css/site.css`). That is correct for
> a custom domain and broken on a `username.github.io/repo/` subpath. Do not judge the design
> from the github.io preview URL — spin it up locally instead.

---

## Gate 1 — Truth. Nothing publishes with a false claim on it.

These are the things on the site that are only true if you confirm them. **This gate is the one
that actually matters**; the rest is plumbing.

- [ ] **`hamza@inheritingislam.com` receives mail.** Every conversion on the site — the contact
      form, the app waitlist, Qur'an enrolment, the podcast guest link — composes an email to that
      address. Your notes have `inheritingislam@gmail.com` as the working address. Send yourself a
      test before launch or every enquiry falls in a hole.
- [ ] **The phone number is public on all nine pages.** `(470) 404-0648`, as a `tel:` link.
      Confirm you want that.
- [ ] **Al-Maun.** The case study says *built, tested, handed over — go-live is the domain switch
      on their side.* That is true today. If it goes live first, update it (search `go-live` in
      `studio/almaun/index.html` and `index.html`) before this site publishes.
- [ ] **Capacity.** `/contact/` says "a small number of builds at a time." Replace with your real
      number — a specific one converts noticeably better.
- [ ] **The Qur'an hero image.** The hadith on the wooden board reads
      خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ. I checked the letterforms and diacritics
      and they are correct — but you taught this, so give it your own look. It is the one image on
      the site where an error would matter.
- [ ] **App statuses.** Seven apps, none shipped. If any status changed, `/apps/` changes with it.
- [ ] **Saif al-Ummah is provisional and needs your words.** It is listed at `Concept` and
      described only as "a game… an older idea that has not been given its final shape." I had no
      source material on it — that description is inferred from your having stepped away from a 3D
      Steam build, not from anything you wrote. Confirm the status, and give me one true sentence
      about what it is. If it is further along than Concept, the page currently understates it; if
      it is shelved, it should come off.

## Gate 2 — Technical. Automated, so it stays true.

`tools/check.py` runs on every push and pull request, and blocks the deploy on failure. It checks
dead links and anchors, one `<h1>` per page, landmarks, alt text, form labels, `lang="ar"` on every
Arabic string, third-party requests, and phrases that would overclaim.

```bash
python3 tools/check.py          # < 1s, no browser needed
```

The heavier sweep needs Chrome and runs locally when you change layout or colour:

```bash
python3 -m http.server 8080                     # terminal one
python3 tools/render-audit.py http://localhost:8080 "/,/studio/,/apps/,/quran/"
```

It renders every page at 1440px and 390px in both themes and fails on horizontal overflow.

- [ ] `tools/check.py` green
- [ ] Render audit green at 390px — a large share of this audience is on a phone
- [ ] Open it on a real phone in daylight. Nothing replaces this.
- [ ] Tab through `/contact/` with the keyboard only; the form must be completable
- [ ] Submit the form and confirm your mail client opens with the message written out

## Gate 3 — DNS and hosting.

1. **Enable Pages** — Settings → Pages → Source: **GitHub Actions**. The workflow is already
   committed.
2. **Add the custom domain** — Settings → Pages → Custom domain → `inheritingislam.com` → Save.
   The `CNAME` file in the repo already declares it.
3. **Point DNS at GitHub** — at your registrar:

   | Type | Name | Value |
   |---|---|---|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | CNAME | `www` | `inheriting-islam.github.io.` |

   Leave the existing `itqan` subdomain record alone — it is a separate deployment.
4. **Wait for the certificate.** GitHub issues it automatically once DNS resolves; usually
   minutes, sometimes a few hours. Then tick **Enforce HTTPS**. Do not skip this.
5. **Verify the domain** in the organisation settings to prevent takeover of the subdomain.

- [ ] `https://inheritingislam.com` serves the site
- [ ] `https://www.inheritingislam.com` redirects to the apex
- [ ] Enforce HTTPS is on
- [ ] `https://inheritingislam.com/sitemap.xml` and `/robots.txt` load

## Gate 4 — Launch, and the week after.

- [ ] Paste a page URL into WhatsApp and iMessage — the share card in `assets/img/og-card.png`
      should appear
- [ ] Submit `sitemap.xml` to Google Search Console
- [ ] Deliberately hit a bad URL and confirm `404.html` renders
- [ ] Send the link to two people who are not you and watch them use it without helping
- [ ] Only then: send it to imams and boards

**Not doing at launch, on purpose:** analytics. The site says it carries no trackers and no
cookies, and that claim is worth more than the numbers. If you later want to know traffic, use a
server-side or log-based tool that does not touch the visitor — and update the footer copy the same
day, or the claim becomes a lie.

---

## Making changes afterwards

```bash
git checkout -b some-change
# edit
python3 tools/check.py
git commit -am "…" && git push -u origin some-change
gh pr create --fill
```

The checks run on the pull request. Merging to `main` deploys automatically.

Header, footer and nav are duplicated across the nine pages on purpose — there is no build step,
so a change to one is a change to all nine. `tools/check.py` will catch a link you broke; it cannot
catch a nav item you forgot to add in eight places.

## What is deliberately not in this repo

`_internal/` is git-ignored. It holds the build notes — the Al-Maun launch-status detail, the
second client still mid-deal, the pricing argument against the planning docs, and the open naming
questions. That is commercial strategy, and this repo is public.

If you want it in GitHub, say so and it goes in a **private** repo. Do not move it here.
