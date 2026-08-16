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
> from the github.io preview URL — spin it up locally instead. Now that the custom domain is
> attached, that preview URL redirects here anyway.

**What actually gets published is `_site/`, not the repo.** `tools/stage.sh` builds it, and CI runs
that same script. It drops `DEPLOY.md`, `README.md`, `docs/`, `tools/` and `.claude/` — otherwise
this file would answer 200 on the production domain, along with the sales one-pagers in `tools/`,
which `check.py` deliberately never audits. A CI gate fails the build if any of them reappear.

```bash
tools/stage.sh                                    # builds ./_site
python3 -m http.server 8099 --directory _site     # this is what visitors get
```

`CNAME` ships in the artifact and `stage.sh` refuses to build without it — but **it does not attach
the custom domain on its own.** That is worth stating plainly because the opposite is widely
assumed, including by an earlier draft of this file. On an Actions-built site the domain has to be
set on the Pages settings screen (or via the API); the file deployed cleanly for hours while Pages
still reported `cname: null` and served "Site not found".

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

It also checks that every page carries the **Content-Security-Policy** meta, byte for byte. Pages
cannot send response headers, so the policy rides in the HTML. `'unsafe-inline'` is unavoidable
while the theme script and 190 style attributes are inline, but `default-src 'self'` and
`connect-src 'none'` shut out every other origin — which is what turns "no trackers, no
third-party scripts" into something the browser enforces rather than something this repo merely
claims. It cannot set `frame-ancestors`; that needs a real header, which Pages will not do.

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
2. **Set the custom domain explicitly** — Settings → Pages → Custom domain, or
   `gh api -X PUT repos/Inheriting-Islam/inheritingislam.com/pages -f cname=inheritingislam.com`.
   The `CNAME` file in the artifact does *not* do this for you on an Actions-built site.
3. **Point DNS at GitHub.** The nameservers are **Cloudflare** (`ian`/`sharon.ns.cloudflare.com`),
   so this is done in the Cloudflare dashboard, not at the registrar:

   | Type | Name | Value | Proxy |
   |---|---|---|---|
   | A | `@` | `185.199.108.153` | **DNS only** |
   | A | `@` | `185.199.109.153` | **DNS only** |
   | A | `@` | `185.199.110.153` | **DNS only** |
   | A | `@` | `185.199.111.153` | **DNS only** |
   | CNAME | `www` | `inheriting-islam.github.io.` | **DNS only** |

   > **The proxy has to be off — grey cloud, not orange.** This zone defaults to proxied, and the
   > records went in orange the first time. While Cloudflare answers for the domain, GitHub cannot
   > validate it, never issues the certificate, and **Enforce HTTPS stays greyed out permanently**.
   > The tell is a working site with a padlock whose certificate is issued by *Google Trust
   > Services* rather than Let's Encrypt — that is Cloudflare's, not yours, and every visitor is
   > being routed through their edge, which is hard to square with the footer's promise of no
   > third parties.

   `itqan` is a `CNAME` to `inheriting-islam.github.io` — another Pages site, not something that
   needs proxying. It has its own Let's Encrypt certificate and is fine unproxied.

   Do not touch the `MX` record. Mail for `hamza@inheritingislam.com` routes through Google, and
   every conversion on the site depends on it.
4. **Redeploy.** Attaching a domain does not republish the site. Until a deployment runs *after*
   the domain is set, Pages serves "Site not found" on it. `gh workflow run deploy.yml --ref main`.
5. **Wait for the certificate** — usually minutes once DNS is correct.

   > **If it never arrives, the domain is stuck on a cached failed check.** This happened here: the
   > domain was first attached while DNS was still proxied, and the Pages API then carried no
   > `https_certificate` object at all. Re-saving the *same* `cname` is a no-op and triggers
   > nothing. Clear it and set it again — the certificate issued within a minute:
   >
   > ```bash
   > echo '{"cname": null}' | gh api -X PUT repos/Inheriting-Islam/inheritingislam.com/pages --input -
   > gh api -X PUT repos/Inheriting-Islam/inheritingislam.com/pages -f cname=inheritingislam.com
   > ```

6. **Tick Enforce HTTPS** once the certificate exists —
   `gh api -X PUT …/pages -F https_enforced=true`. Do not skip this.
7. **Verify the domain** in the organisation settings to prevent takeover of a subdomain. This is
   browser-only; there is no REST endpoint for it, and none for the org 2FA requirement either.

- [x] `https://inheritingislam.com` serves the site — all 17 pages 200
- [x] `https://www.inheritingislam.com` redirects to the apex; `http://` redirects to `https://`
- [x] Enforce HTTPS is on; certificate is Let's Encrypt, covering the apex and `www`
- [x] `https://inheritingislam.com/sitemap.xml` and `/robots.txt` load
- [ ] Verify the domain in organisation settings
- [ ] Require 2FA org-wide — **confirm Khadija has 2FA on first**, or GitHub removes her from the org

> GitHub Pages sends **no HSTS header** on custom domains and cannot be made to. Measured, not
> assumed. `frame-ancestors` is likewise unavailable, since a meta tag cannot set it.

## Gate 4 — Launch, and the week after.

- [ ] Paste a page URL into WhatsApp and iMessage — the share card in `assets/img/og-card.png`
      should appear
- [ ] Submit `sitemap.xml` to Google Search Console
- [x] Deliberately hit a bad URL and confirm `404.html` renders — verified on the live domain
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
