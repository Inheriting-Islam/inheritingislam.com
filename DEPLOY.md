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

**What actually gets published is `_site/`, not the repo.** `tools/stage.sh` builds it, and CI runs
that same script. It drops `DEPLOY.md`, `README.md`, `docs/` and `tools/` — otherwise this file
would answer 200 on the production domain, along with the sales one-pagers in `tools/`, which
`check.py` deliberately never audits. A CI gate fails the build if any of them reappear.

```bash
tools/stage.sh                                    # builds ./_site
python3 -m http.server 8099 --directory _site     # this is what visitors get
```

`CNAME` is what attaches the custom domain. Because the artifact comes from Actions rather than a
branch, the domain lives in that file — delete it and the domain silently detaches on the next
deploy. `stage.sh` refuses to build without it.

---

## Gate 1 — Truth. Nothing publishes with a false claim on it.

These are the things on the site that are only true if you confirm them. **This gate is the one
that actually matters**; the rest is plumbing.

- [x] **`hamza@inheritingislam.com` receives mail.** Every conversion on the site — the contact
      form, the app waitlist, Qur'an enrolment, the podcast guest link — composes an email to that
      address. Confirmed: the domain's MX points at `smtp.google.com` and the mailbox is a live
      Google Workspace account. Still send one real test through a form before launch; the DNS
      being right is not the same as the message arriving.
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
- [x] **App statuses.** Three apps in progress, four set down and named as such, none shipped.
      Corrected in `2914be9`. If any status changes, `/apps/` changes with it.
- [x] **Saif al-Ummah.** Given its own words in `01be35c` — set down, not stopped.

## Gate 2 — Technical. Automated, so it stays true.

`tools/check.py` runs on every push and pull request, and blocks the deploy on failure. It checks
dead links and anchors, one `<h1>` per page, landmarks, alt text, form labels, `lang="ar"` on every
Arabic string, third-party requests, phrases that would overclaim, and that `sitemap.xml` lists
every indexable page and nothing else — a hand-written sitemap drifts the moment you add a page,
and a crawler is the last thing to tell you. `/quran/verify/` is `noindex`, so it is correctly
absent.

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

1. **Pages is already enabled** — Source: **GitHub Actions**, and deploys are green. Nothing to do.
2. **The custom domain comes from the `CNAME` file**, not the settings screen. It ships in the
   artifact, so the domain attaches itself on the next deploy.
3. **Point DNS at GitHub.** The nameservers are **Cloudflare** (`ian`/`sharon.ns.cloudflare.com`),
   so this is done in the Cloudflare dashboard, not at the registrar:

   | Type | Name | Value | Proxy |
   |---|---|---|---|
   | A | `@` | `185.199.108.153` | **DNS only** |
   | A | `@` | `185.199.109.153` | **DNS only** |
   | A | `@` | `185.199.110.153` | **DNS only** |
   | A | `@` | `185.199.111.153` | **DNS only** |
   | CNAME | `www` | `inheriting-islam.github.io.` | **DNS only** |

   > **The proxy has to be off — grey cloud, not orange.** This zone defaults to proxied;
   > `itqan.inheritingislam.com` resolves to Cloudflare IPs today. If these records are proxied,
   > GitHub cannot validate the domain, never issues the certificate, and **Enforce HTTPS stays
   > greyed out permanently**. Turn the proxy on later if you want it, but only after the
   > certificate exists, and set SSL mode to Full (strict) when you do.

   Leave the existing `itqan` record alone — it is a separate deployment.

   Do not touch the `MX` record. Mail for `hamza@inheritingislam.com` routes through Google, and
   every conversion on the site depends on it.
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
