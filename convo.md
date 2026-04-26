# Static Web Builder Skill — Conversation Log
## Context for continuing in a new session

This document captures all decisions, rules, and pending changes from the skill-building conversation between Mike and Claude.

---

## What We Built

A Claude skill (`static-web-builder`) that builds complete multi-page static websites for local service businesses through a guided conversational interview. No form inputs — Claude asks for everything it needs.

**Current skill version:** v45 (static-web-builder-v45.skill)  
**Skill location:** `/home/claude/static-web-builder/SKILL.md`  
**Skill file:** downloadable as `static-web-builder.skill`

---

## Skill Overview

- **Conversational intake** — 6 rounds of guided questions, Claude asks everything
- **Multi-page output** — homepage, service pages, Privacy Policy, T&C, Spanish versions
- **Fixed 10-section layout** on all pages except Privacy Policy and T&C
- **Gemini API image generation** — all images generated via Python script using `.env` key
- **Bilingual support** — English + Spanish with regional dialect control
- **Direct-response copywriting** — visitor-first language, pain points, objections, CTAs
- **Full SEO** — meta tags, OG tags, Twitter Cards, JSON-LD schema, sitemap, robots.txt

---

## File Structure Output

```
project-folder/
├── index.html                                    ← English homepage → served at /
├── [service-slug]/index.html                     ← One folder per service page → served at /[service-slug]/
├── [spanish-home-slug]/index.html                ← Spanish homepage folder → served at /[spanish-home-slug]/
├── [servicio-slug]/index.html                    ← Spanish service pages → served at /[servicio-slug]/
├── privacy-policy/index.html                     ← served at /privacy-policy/
├── terms-and-conditions/index.html               ← served at /terms-and-conditions/
├── politica-de-privacidad/index.html             ← served at /politica-de-privacidad/
├── terminos-y-condiciones/index.html             ← served at /terminos-y-condiciones/
├── 404.html                                      ← Custom 404 page (stays at root — served by the host on 404)
├── sitemap.xml
├── robots.txt
├── .gitignore
├── css/styles.css
├── js/main.js
├── images/
├── scripts/generate_images.py
├── scripts/validate_env.py
├── scripts/images_manifest.json
└── .env  (never deploy)
```

**Clean URL convention:** every page (except `index.html` at root and `404.html`) lives inside its own folder as `index.html`. URLs are extensionless (e.g. `/drain-cleaning/` instead of `/drain-cleaning.html`). Works natively on GitHub Pages, Netlify, Vercel, Cloudflare Pages, etc. All internal links, canonicals, sitemap entries, and `hreflang` references use the folder URL with trailing slash.

---

## The 6-Round Client Interview

### Round 1 — Business Identity
- **FIRST QUESTION:** Is this a **local** business (one physical location) or **national/multi-location** business (running ads across multiple areas, no single address)? → stores `BUSINESS_TYPE` = `local` | `national`
- Business name, industry, phone, email, domain (always asked)
- **If `BUSINESS_TYPE = local`:** city, state, full address, Google Maps iframe
- **If `BUSINESS_TYPE = national`:** skip city/state/address/Google Maps (not asked)

### Round 2 — Services
- **Upfront:** Claude immediately shows a **numbered list of the top 10 most popular services** in the client's industry, ordered from most popular (1) to least popular (10). Claude says: *"These are the 10 most popular services in your industry, listed from most to least popular. Would you like to expand this list with additional services?"*
- If the client wants to expand, Claude adds more numbered options (continuing from 11, 12, 13...) relevant to the industry.
- **Client selects by number only** — no need to type service names. Comma or space-separated numbers accepted (e.g. `1, 3, 5, 7` or `1 3 5 7`).
- **Main service selection:** Claude recommends a **main service** — the umbrella service that becomes the homepage theme (e.g. "Plumbing Services"). Client confirms by number or picks a different one.
- Stores `MAIN_SERVICE` (homepage theme) and `SERVICES` (sub-service pages).
- Homepage is themed around `MAIN_SERVICE`, references all sub-services → hub-and-spoke SEO.
- **If `BUSINESS_TYPE = local`:** Ask: add location to filenames? (affects filename, `<title>`, `<h1>`)
- **If `BUSINESS_TYPE = national`:** Skip location question — clean slugs, no geo modifiers anywhere

### Round 3 — Branding
- Logo for light backgrounds (URL / filename / upload / none), Logo for dark backgrounds (same options)
- Favicon for light browser themes (PNG, transparent bg), Favicon for dark browser themes (PNG, transparent bg) — swapped at runtime via a tiny JS listener on `prefers-color-scheme`. Chrome ignores `media` attributes on favicon `<link>` tags, so JS swap is the only cross-browser reliable approach. If the client only has one PNG, both slots use the same file (no theme adaptation in that case).
- Main HEX color, hover HEX color
- Tagline (or Claude generates one)
- Fonts: default Montserrat (headings) + Open Sans (body), client can override

### Round 4 — Features
- Booking widget? (Calendly etc.)
- Spanish version? → ask regional dialect (Mexican Spanish, Colombian Spanish, etc.)
- `MODAL_WEBHOOK_URL` — Pabbly Connect webhook for the modal popup (Hero, Banner, Footer)

### Round 5 — Social Proof & Extras
- Reviews: client provides or Claude generates (3 cards)
- Hero image or gradient background
- FAQs (or Claude generates 6)
- OG social share image: client provides or Claude generates via Gemini
- *(Social media profiles removed — no longer asked)*

### Round 6 — Audience & Market Research
- Ideal customer, pain points, fears/objections, dream outcome
- Proof/credentials, competitive edge, offer, urgency

### Research Synthesis → Page Conversion Strategy
- Present brief to client, get approval, then build

---

## Fixed Page Layout (all pages except Privacy Policy and T&C)

1. Navigation (Header)
2. Hero
3. Why Us
4. About Us
5. Reviews
6. Banner
7. Services
8. Steps To Work With Us
9. FAQs
10. Footer

---

## Key Design Rules

- Section backgrounds alternate: white (`#ffffff`) ↔ gray (`#f2f2f2`)
- Banner: always `--color-primary !important`
- Footer: always `#282828 !important`
- Hero: `--color-primary` background with `hero-bg.webp` background image
- All CSS in `css/styles.css`, all JS in `js/main.js`
- No inline styles or scripts
- All sections: `position: static` — only nav uses `sticky`
- All section paddings identical via CSS variables

## Typography Defaults
- Headings: Montserrat 800, capitalize, left-aligned
- Body: Open Sans
- Review names: Dancing Script 600 (cursive)
- h2: same size across entire page (`clamp(1.5rem, 3vw, 2.25rem)`)
- h3: same size across entire page (`clamp(1.1rem, 2vw, 1.4rem)`)

## Colors
```css
:root {
  --color-primary: /* client HEX */;
  --color-hover: /* client HEX */;
  --color-primary-light: /* derived */;
  --color-accent: /* complementary */;
  --color-text-dark: #2d2d2d;
  --color-text-light: #ffffff;
  --color-text-muted: #6b6b6b;
  --color-cta-text: #ffffff;
  --color-bg-white: #ffffff;
  --color-bg-gray: #f2f2f2;
  --color-border: /* derived */;
}
```

---

## Navigation Spec

- Logo (50px wide, light version for dark backgrounds, dark version for light backgrounds) + company name (22px, 800, uppercase, `--color-primary`) → both link to `/`
- Menu: Home | Services ▾ | About Us ▾
- No buttons in nav
- All links lowercase with hyphens, absolute paths from root
- Text: `--color-primary` on white, hover: `--color-hover` background + white text
- Services dropdown: anchor text = service name only, href = `/[service-slug]/` (extensionless, trailing slash)
- About Us dropdown: "About Us" → `/#about-us` (English) or `/SPANISH_HOME_FILENAME#about-us` (Spanish) | Privacy Policy | Terms & Conditions
- Hamburger at < 750px
- Dropdowns align to LEFT edge of parent item
- Height minimal: `padding: 6px 0`

---

## Hero Section Spec

- Background: `hero-bg.webp` (16:9, 2K, Gemini generated), `background-size: cover`
- `.hero-content`: `width: 100%`, no max-width, `background: rgba(0,0,0,0.75)`
- `h1.hero-label`: service page name, 18px, 800, uppercase, `--color-primary`
- `h2.hero-headline`: 3rem, 800, white — pain point or desired outcome
- `p.hero-body`: 1.5rem, 600, white — 1-2 sentences
- Two CTA buttons centered: Primary (`tel:PHONE`) + Secondary (triggers modal)
- Buttons stack vertically when space runs out; `width: 100%` at < 700px
- **Same spec applies to service pages**

---

## Modal Popup Spec

- Triggered by secondary CTA button (`data-modal="hero-modal"`) in: **Hero, Banner, and Footer**
- 2-3 qualifying questions (industry-specific, Claude generates and presents to client first)
- Step 1: service type (multiple choice)
- Step 2: qualifying follow-up (multiple choice or text)
- Step 3: Full Name, Phone, Email (all required)
- Submits to `MODAL_WEBHOOK_URL` (Pabbly Connect)
- `"source": "hero_modal"` in payload
- After successful submission → show "Thank You" step inside modal ("Thank you! We'll be in contact soon."). Auto-closes after a few seconds or on user click.
- One modal per page, triggered by `data-modal="hero-modal"`
- **No separate contact form section — modal is the only lead capture**

---

## Image Generation

- All images: WebP format, compressed (quality=82, method=6)
- Model: looked up at build time from `ai.google.dev` — never hardcoded
- Script: `scripts/generate_images.py` reads `images_manifest.json`
- Validate key first: `python scripts/validate_env.py`

| Image | Filename | Aspect | Resolution |
|---|---|---|---|
| Hero | `hero-bg.webp` | 16:9 | 2K |
| About Us | `about-us.webp` | 1:1 | 1K |
| Services (×4) | `service-[slug].webp` | 1:1 | 1K |
| Banner | `banner-cta.webp` | 21:9 | 2K |
| Steps | `steps-bg.webp` | 16:9 | 1K |
| OG Share | `og-image.webp` | 16:9 | 1K |

---

## BUSINESS_TYPE Rules (local vs national)

Stored in Round 1 as the first question. Controls all location-aware output:

| Element | `local` mode | `national` mode |
|---|---|---|
| City / state / address | Collected, displayed | Not asked, not displayed |
| Google Maps iframe | Embedded in footer | Skipped |
| Footer layout | Layout A (2-col with map) | Layout B (centered, no map) |
| JSON-LD schema | `LocalBusiness` with full address | `Organization` (no address) |
| Service folder slugs / URLs | Optional location suffix (`/plumbing-phoenix-az/`) | Clean slugs (`/plumbing/`) |
| Services dropdown hrefs | Match filenames | Clean slugs |
| Internal link anchor text | May include location ("Phoenix plumbing services") | Geo-free ("our plumbing services") |
| Page `<title>` tags | Optional `\| City, State` suffix | No geo suffix |
| H1 (`.hero-label`) — SEO service name | `Plumbing Services in Phoenix, AZ` | `Plumbing Services` |
| H2 (`.hero-headline`) — pain point / outcome | May reference location if natural | Problem/benefit-led, geo-free |
| About Us copy | May reference location ("Serving Phoenix since...") | No location references |
| FAQ content | Can include "What areas do you serve?" | Skip geo-specific FAQs |
| Canonical URLs / sitemap | Unchanged | Unchanged |
| `hreflang` tags | Unchanged | Unchanged |

Hub-and-spoke SEO works in both modes — national mode targets service keywords, local mode targets service + city keywords.

---

## Bilingual Rules

- English homepage: `index.html` at root → served at `/`
- Spanish homepage: `[spanish-home-slug]/index.html` — slug derived from Spanish SEO title → served at `/[spanish-home-slug]/` (e.g. `/compania-de-techos-phoenix-az/` for local, or `/compania-de-techos/` for national)
- Spanish service pages: full translations of English service pages, same rules
- Language toggle in the hero, directly above the H1 (not in the nav): ESPAÑOL ↔ ENGLISH with FA7 `fa-language` icon
- `hreflang` tags cross-reference both versions
- Regional Spanish: client specifies (Mexican, Colombian, US neutral, city-level, etc.)
- Spanish filenames: no accents, `ñ`→`n`, lowercase, hyphens

---

## SEO

- `<html lang="en">` / `<html lang="es">` on every page
- Charset + viewport FIRST in `<head>`
- Full OG + Twitter Card tags
- `og:image` 1200×630px
- JSON-LD schema: `LocalBusiness` with full address (if `BUSINESS_TYPE = local`) OR `Organization` (if `BUSINESS_TYPE = national`, no address)
- Canonical, hreflang (use domain if known, placeholder if not)
- `sitemap.xml` — all pages included
- `robots.txt` — blocks `scripts/` and `.env`
- Internal linking: every service page links back to `/` contextually

---

## Section-Specific Specs Completed

| Section | Status |
|---|---|
| Navigation | ✅ Full spec |
| Hero | ✅ Full spec |
| Why Us | ✅ Full spec (3 cards, FA7 icons) |
| About Us | ✅ Full spec (2-col, Gemini image 1:1) |
| Reviews | ✅ Full spec (3 cards, fa-quote-left, Dancing Script) |
| Banner | ✅ Full spec (`--color-primary !important`, black primary btn) |
| Services | ✅ Full spec (2-per-row grid, Gemini images 1:1, research first) |
| Steps To Work With Us | ✅ Full spec (3 cards, FA7 icons) |
| FAQs | ✅ Full spec (6 items, accordion, `--color-primary` question bg) |
| Footer | ✅ Full spec (Layout A: 2-col with map / Layout B: centered, `#282828 !important`) |
| Privacy Policy | ✅ Full spec (11 sections) |
| Terms & Conditions | ✅ Full spec (12 sections) |

---

## Font Awesome 7

- CDN: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css`
- Free includes: Solid (`fa-solid`) + Brands (`fa-brands`) only
- Always verify icon names before use — wrong names render as blank squares
- Safe FA7 Free solid icons: `fa-check`, `fa-shield`, `fa-star`, `fa-clock`, `fa-phone`, `fa-wrench`, `fa-bolt`, `fa-house`, `fa-user`, `fa-thumbs-up`, `fa-award`, `fa-handshake`, `fa-tools`, `fa-leaf`, `fa-truck`, `fa-certificate`, `fa-dollar-sign`, `fa-heart`, `fa-circle-check`, `fa-triangle-exclamation`, `fa-quote-left`, `fa-chevron-down`, `fa-calendar-check`, `fa-clipboard-list`

---

## Completed Changes (v44)

1. ✅ **Removed social media profiles from Round 5** — no social media questions asked during interview
2. ✅ **Removed `PABBLY_HOOK` / contact form from Round 4** — deleted the contact form question, removed the entire "Step 4: Multi-Step Contact Form Spec" section, cleaned up all `PABBLY_HOOK` references. Modal is now the only lead capture mechanism.
3. ✅ **Modal trigger confirmed in Hero, Banner, and Footer** — HTML already had `data-modal="hero-modal"` in all three; updated the Modal Behavior Rules description and Round 4 webhook question to explicitly state all three locations.
4. ~~Fix modal timing in Round 4~~ — client said timing doesn't matter, skipped.
5. ~~Spanish service pages~~ — client unclear on intent, skipped for now.
6. ✅ **Updated YAML frontmatter description** — now reflects multi-page output, modal-based lead capture, no contact form references.

## Changes in v45

7. ✅ **Overhauled Round 2 — Services** — Claude now shows `SERVICE_COUNT + 4` numbered suggestions (4 extras since client may not offer all). Claude recommends a **main service** (umbrella service) that becomes the homepage theme. Client picks by number or name. Stores `MAIN_SERVICE` and `SERVICES`. Homepage is themed around `MAIN_SERVICE` and references all sub-services (hub-and-spoke SEO).

## Changes in v46 (Pending)

8. **Modal thank you screen** — After form submission, display a "Thank You" step inside the modal (not a separate page — this is a static site with no server). Message: "Thank you! We'll be in contact soon." Modal closes after a few seconds or on user click.
9. **Alt text on all `<img>` tags** — Every image must have descriptive alt text relevant to the image content and section context. No empty `alt=""` except for purely decorative images.
10. **Performance optimizations** — Add all of the following:
    - `loading="lazy"` on all images below the fold
    - `font-display: swap` on all Google Fonts imports
    - `<link rel="preconnect">` hints for CDN resources (Google Fonts, Font Awesome CDN)
    - Minified CSS (`styles.min.css`) and JS (`main.min.js`) for production
11. **Service page content uniqueness (confirmed)** — Every service page has all 10 sections rewritten uniquely for that service. No repeated/duplicate content across pages.
12. **Phone numbers are `tel:` links everywhere** — All phone numbers across all pages (hero, banner, footer, etc.) are wrapped in `<a href="tel:PHONE">` and trigger a call on mobile.
13. **404 page** — `404.html` included in file structure. Branded with site nav/footer, friendly message, and link back to homepage. Works automatically on GitHub Pages, Netlify, Vercel, and Cloudflare Pages.
14. **`BUSINESS_TYPE` flag (local vs national)** — Round 1 now starts by asking whether the business is local (one physical location) or national/multi-location (runs ads across areas, no single address). Controls all location-aware output: city/state/address collection, Google Maps iframe, footer layout, JSON-LD schema type (`LocalBusiness` vs `Organization`), service filenames/slugs, internal link anchor text, `<title>` / H1 / hero copy, About Us location references, FAQ content. National mode strips all geo modifiers; hub-and-spoke SEO still works. See dedicated "BUSINESS_TYPE Rules" section.
15. **Round 2 flow overhauled (again)** — Claude now shows the top 10 most popular services in the industry upfront (numbered, ranked most → least popular), asks if the client wants to expand the list, and has the client select **by number only**. No typing service names. Replaces the old `SERVICE_COUNT + 4` approach.
16. **H1 rule enforcement (bug fix)** — Test build put `BUSINESS_NAME` as the H1 on the homepage. SKILL.md only mentioned the H1 rule in passing (line 145). Added a dedicated "CRITICAL H1 RULE" section with an explicit table: H1 is always the SEO service name (with optional location suffix in local mode), never the business name. Business name only appears in the nav logo area and the footer. Also cleaned up the BUSINESS_TYPE Rules table to separate H1 (service name) from H2 hero headline (pain point / outcome).
17. **Contact display rule (bug fix — anti-spam)** — Test build displayed phone and email as plaintext below the hero buttons. Added "CRITICAL CONTACT DISPLAY RULE" section in SKILL.md: email never appears in the footer, hero, nav, homepage, or service pages. Phone only appears inside `tel:` button links on those pages. Both phone AND email may appear in plaintext in Privacy Policy / T&C contact sections (no obfuscation needed — legal context, low spam risk). Explicit list of forbidden and allowed patterns. Hero has exactly 2 CTA buttons and nothing below them. Footer has logo + name + 2 CTA buttons + map, no contact info text.
18. **Full Spanish translations for ALL pages** — Every single page has an equivalent Spanish page, including Privacy Policy (`/politica-de-privacidad/`) and Terms & Conditions (`/terminos-y-condiciones/`). These are full translations, not copies of English text.
19. **Paragraph width rule (bug fix)** — Test build had narrow paragraphs due to typography guidance saying "Paragraph max-width: `65ch`". Rewrote the rule: paragraphs ALWAYS take 100% of the parent container width. No max-width caps (`65ch`, `800px`, etc.) on paragraphs in section content. Line-length readability is handled by the `.container` max-width at the section level (`1100px`). Exceptions: 2-column subcontainer layouts (e.g. About Us text column) and the Banner CTA text (centered).
20. **Container max-width raised to 1200px** — Changed `--container-max-width` from `1100px` to `1200px` so sections have more horizontal room on desktop. Updated reference in the paragraph width rule.
21. **`.hero-content` padding set to 20px** — Final value: `padding: 20px; margin: 0;` on `.hero-content`. (Briefly considered zero padding, then reverted to 20px on all sides.)
22. **Language toggle moved from nav to hero, new icon, plain-link styling** — Previously: button in the nav with 🌐 emoji, border, padding. Now: lives inside `.hero-content` as the first child, directly above the H1. Uses FA7 `fa-language` icon. Styled as a **plain text link — no border, no background, no padding**. White on the dark hero overlay. On hover, text + icon scale up 10% (`transform: scale(1.1)`) and turn `--color-primary`. Grows from the left (`transform-origin: left center`). Same behavior on Privacy Policy / T&C / 404 pages, but default color is `--color-text-dark` on the light background. Nav no longer contains the toggle.
23. **Clean URLs (no `.html`)** — All pages except the root `index.html` and `404.html` live inside their own folder as `index.html`. URLs are extensionless with trailing slashes: `/drain-cleaning/` instead of `/drain-cleaning.html`. Applies to all internal links, `href`s, canonicals, sitemap entries, `hreflang` references, and Services dropdown. Works natively on GitHub Pages, Netlify, Vercel, Cloudflare Pages.
24. **No-pricing rule broadened site-wide** — Previously "No pricing discussed in FAQs" only. Now a universal rule: no dollar amounts, no price ranges, no numeric cost references in any section or language. Added dedicated "CRITICAL NO-PRICING RULE" section in SKILL.md with forbidden/allowed examples. Positioning language still allowed ("upfront pricing", "free estimates", "no hidden fees"). Interview question at line 411 annotated so the client knows pricing info shared is only used for positioning tone, never published verbatim.
25. **Favicon theme-adaptation via JS swap (bug fix)** — Chrome ignores `media` attributes on favicon `<link>` tags, so the original dual-favicon approach using `prefers-color-scheme` media queries didn't work — user reported the light-theme favicon showing on their dark-theme Chrome. Switched to a tiny JS listener in `js/main.js` that watches `prefers-color-scheme` and swaps the `<link id="favicon">` href between `FAVICON_LIGHT` and `FAVICON_DARK` on page load and on theme change. Works in Chrome, Firefox, Safari, Edge. Updated the Round 3 favicon question to explicitly collect two PNGs (light + dark) and added a fallback path when only one is provided. Storage renamed: `FAVICON` → `FAVICON_LIGHT` + `FAVICON_DARK`.

## Out of Scope (handled via Claude Code post-build)

- Google Analytics / GA4 / GTM
- Facebook / Meta Pixel
- Any other tracking pixels or analytics
- These are client-specific add-ons, not part of the default skill build

---

## Copywriting Philosophy

- Visitor-first language: "you/your" dominant, avoid "we/our/us"
- Every section title speaks to a pain point or benefit
- Every h3 is outcome-driven, not a label
- **No specific pricing discussed anywhere on the site** — no dollar amounts, no price ranges, no "starting at $X" in the hero, services, banner, FAQs, About, or anywhere else. Positioning phrases like "upfront pricing", "free estimates", "no hidden fees", and "you'll know the exact price before work begins" are allowed — those set expectations without committing to numbers.
- 40-60 word intro paragraphs on Why Us, Reviews, Services, Steps, FAQs
- About Us body: 100-130 words, 2 paragraphs minimum
- Reviews: 3 cards, h3 titles capture the emotional core of each review
- Hub-and-spoke SEO: every service page links back to homepage contextually

---

## Reference Files in Skill

- `references/industry-services.md` — services by vertical for Round 2 suggestions
- `references/form-templates.md` — multi-step form patterns
- `references/section-snippets.md` — reusable CSS/JS patterns
- `scripts/generate_images.py` — Gemini image generation
- `scripts/validate_env.py` — API key validation
- `scripts/images_manifest_example.json` — example manifest

---

## How to Continue

1. Install `static-web-builder.skill` in Claude
2. Reference this `convo.md` for context
3. All v43 pending changes are resolved — skill is at v44
4. Next step: do a final test build with a sample business


# ═══════════════════════════════════════════════════════════════════════════
# Firefly Rise — Project Build Log
# ═══════════════════════════════════════════════════════════════════════════

This section is the project's running changelog — every change made to the
fireflyrise.github.io repo, what changed, and why. Append a new entry every
time we ship something. The repo is a portable record, so this file follows
us across machines.

**Project context:** Firefly Rise is a national US digital marketing agency
that works exclusively with home-service contractors (plumbers, HVAC,
roofers, landscapers, etc.). Site is a static, bilingual (EN/ES) build
deployed on GitHub Pages at fireflyrise.com.

**Tech stack:**
- Static HTML/CSS/JS (no framework)
- Templated via `scripts/build_site.py` from `scripts/site_data.py` and
  `scripts/faqs_data.py` — one source of truth, 27 generated pages
- Images generated via Gemini 2.5 Flash Image (`scripts/generate_images.py`)
- Pabbly Connect webhook for lead capture (URL loaded from `.env` at build)
- GitHub Pages hosting + CNAME → fireflyrise.com

---

## Build log (newest at top)

### 2026-04-24 — Phone input auto-formatter (commit `f61b7f4`)
**What:** Modal phone field now formats US numbers live as the visitor
types: `6` → `(6`, `602` → `(602`, `6028290009` → `(602) 829-0009`.
Paste handler strips country codes (`+1 …`) and re-formats. Added
`inputmode="numeric"` (mobile numeric keypad), `placeholder="(123) 456-7890"`,
and `maxlength="14"`.
**Why:** Better UX — visitors don't have to know the format, mobile users
get the right keyboard, and the data hitting Pabbly is consistent.

### 2026-04-24 — Honeypot anti-spam field (commit `9dfe36d`)
**What:** Added a hidden `website` text input to the modal positioned at
`left: -10000px` (off-screen, not `display:none` because savvy bots skip
those). On submit, JS reads the field; if non-empty (a bot filled it),
shows a fake success state and skips the POST entirely — saves a Pabbly
task credit and gives the bot zero feedback that it was caught.
**Why:** The Pabbly webhook URL is necessarily public (baked into the page
HTML — that's how Pabbly is meant to be used with static sites). The
honeypot is the cheapest, most effective first line of defense against
basic bot scrapers. Verified end-to-end in the browser — bot path skips
fetch; real path POSTs the full payload.
**Future option (not done):** add a Pabbly Filter step that drops payloads
where `website` is non-empty, to catch bots that POST directly to the URL
bypassing the form.

### 2026-04-24 — Pabbly webhook wired in from `.env` (commit `ffd7f1f`)
**What:** `scripts/build_site.py` loads `PABBLY_CONNECT_WEBHOOK` from
`.env` (gitignored) at build time and bakes it into every page's modal
`data-webhook` attribute. JS in `main.js` POSTs the form payload as JSON
to that URL on submit. Falls back to a placeholder string if the env var
is missing.
**Why:** The modal previously had a `REPLACE_WITH_PABBLY_WEBHOOK_URL`
placeholder; with the webhook live, leads flow to Pabbly Connect.
**Note:** The webhook URL ends up in public HTML — that's expected for
Pabbly. The "secret" is the long base64 token in the URL itself.

### 2026-04-24 — Removed Google Ads API design doc (commit `504e197`)
**What:** Deleted `docs/firefly-rise-google-ads-api-tool-design.pdf` and
`scripts/build_design_doc.py`.
**Why:** Mike used the PDF for the Google Ads API Developer Token
application; not needed in the website repo.

### 2026-04-24 — Added Google Ads API design doc PDF (commit `1f81ac4`)
**What:** 6-page PDF design document for Google Ads API Developer Token
application, generated by `scripts/build_design_doc.py` (ReportLab).
Sections: Tool Overview, Architecture, Users/UI, Data Flow, API Operations,
Authentication, Use Cases, Security, Compliance.
**Why:** Mike's previous Developer Token application was rejected because
the website wasn't live yet. Now that the site is live, the application
needs supporting design docs.

### 2026-04-24 — Aligned with SKILL updates (commit `a7edfb9`)
After Mike updated `SKILL.md` (commit `7694ea7`) with new strict rules,
this commit brought the site into compliance:
- **Favicon:** Replaced the four `<link rel="icon" media="...">` tags with a
  single `<link id="favicon">` plus a `matchMedia` JS swap in `main.js`.
  Reason: Chrome ignores `media="(prefers-color-scheme:...)"` on favicon
  links; only the JS approach works in all major browsers.
- **Footer:** Stripped to SKILL Layout B spec — logo + business name +
  two CTA buttons + copyright. Removed tagline, service-link nav, and
  legal-link nav (those links are still in the main nav dropdowns).
- **Language toggle on legal/404 pages:** Added `fa-language` toggle above
  the `<h1>` on Privacy Policy, Terms & Conditions (EN+ES), and 404 page.
  Light-bg color variant (`--color-text-dark` default, `--color-primary`
  on hover).
- **Hero `.hero-content`:** Now `display: flex; flex-direction: column;
  align-items: flex-start` so the language toggle's `align-self: flex-start`
  positions correctly.
- **Lang toggle styling:** matches SKILL exactly — `font-size: 0.9rem`,
  icon `1.05rem`, hover `transform: scale(1.1)`. Removed obsolete
  `.hero-lang-toggle` modifier; unified into single `.lang-toggle` class.
- **404 meta description:** Removed the phone number — no plaintext phone
  outside buttons, period.

### 2026-04-23 — Stripped all pricing mentions (commit `e83279f`)
**What:** Scrubbed every dollar amount, price/budget/cost mention, and
"ad spend" reference from user-visible copy. Highlights:
- Reviews: removed `$9,000` from a Google Ads win story; renamed
  "Same Ad Budget" titles → "Same Traffic"; removed "higher prices"
- CRO service rewritten: USP changed from "Double your leads without
  spending another dollar" → "Turn more of your existing visitors into
  booked jobs"
- Deleted the "How much do I need to spend on ads?" Q&A entirely (it
  listed `$1,500–$5,000` ranges); replaced with "How will I know if my
  ads are working?"
- Spanish mirrors: `presupuesto`, `precio`, `gasto`, `costo`, `dólar`
  all removed/rephrased
- Removed `priceRange: "$$"` from JSON-LD
- T&C: "Final pricing and scope" → "Final scope and terms"
**Why:** SKILL rule: pricing is never discussed anywhere on the site.
Verified with `scripts/scan_pricing.py` (returns 0 matches).

### 2026-04-20 — Language toggle restyled as plain link (commit `683ee9b`)
**What:** Hero language toggle no longer looks like a button — no border,
no background, no padding. White text + icon by default; on hover it
scales to 108% (later bumped to 110% per SKILL) and turns
`--color-primary`. Smooth `transform-origin: left center` so it grows
rightward.
**Why:** Mike requested a non-button look — a link that becomes more
prominent on hover.

### 2026-04-20 — Language toggle moved to hero, fa-language icon (commit `e8ab575`)
**What:** Removed language toggle from the nav. Added it inside the hero
`.hero-content` directly above the `<h1>` on every page. Replaced the
🌐 emoji with Font Awesome 7 `fa-solid fa-language` (renders consistently
across devices).
**Why:** Mike requested a more prominent placement and a real icon
instead of an emoji that depends on OS font availability.

### 2026-04-19 — Hero content padding 20px (commits `ad17aea`, `5297fcb`)
**What:** First removed all padding/margin from `.hero-content`, then
restored as `padding: 20px` on all sides.
**Why:** Mike changed his mind mid-stream — wanted no padding initially,
then settled on 20px.

### 2026-04-19 — Container max-width 1200px (commit `824b5bc`)
**What:** Bumped `--container-max-width` from 1100px to 1200px.
**Why:** Mike wanted more horizontal room across all sections.

### 2026-04-19 — Removed paragraph max-widths (commit `0d3dec7`)
**What:** Dropped global `p { max-width: 65ch }`, `.section-intro
{ max-width: 75ch }`, and `.hero-body { max-width: 65ch }`.
**Why:** Mike noticed paragraphs looked "chopped off and ugly" — they
were narrower than the surrounding headings/cards. Now all body copy
fills the full container width.

### 2026-04-19 — H1 brand name stripped (commit `ce7c6d1`)
**What:** `<h1>` on every page now drops the business-name portion that
the `<title>` tag carries. E.g. `<title>` is "Firefly Rise | Home
Services Digital Marketing Agency" but `<h1>` is just "Home Services
Digital Marketing Agency".
**Why:** SKILL rule + Mike's directive: H1 is the SEO service name,
never the business name. Title keeps brand for search results;
H1 stays clean on-page.

### 2026-04-19 — Clean URLs, no .html (commit `d71a122`)
**What:** Every page (except root `index.html` and `404.html`) is now
`[slug]/index.html` and links use `/[slug]/` with trailing slash. No
`.html` extensions anywhere in URLs, sitemap, canonical, or hreflang.
Build helpers `clean_url(slug)` and `clean_file(slug)` keep the
slug→URL/path mapping consistent.
**Why:** Mike requested cleaner URLs. Standard pattern that works on
any host serving `index.html` for folder requests.

### 2026-04-19 — Initial full site build (commit `090326f`)
**What:** First full deployment. 27 HTML pages (1 EN home + 1 ES home
+ 10 EN service pages + 10 ES service pages + 2 EN legal + 2 ES legal
+ 404), 35 Gemini-generated WebP images, css/styles.css, js/main.js,
sitemap, robots, gitignore. Built from `scripts/build_site.py` reading
`scripts/site_data.py` + `scripts/faqs_data.py`.
**Decisions made during the interview:**
- 10 services confirmed (Google Ads, Facebook/Meta Ads, Website Design,
  Landing Pages, Lead Gen, Reputation Management, GBP Optimization, CRO,
  Call Tracking, Branding & Logo Design)
- Main service: "Home Services Digital Marketing"
- National (no specific city) — clean URLs, no location-in-filenames
- Brand color `#ff7200`, hover `#ffae00`
- Bilingual: English + Mexican/US-Neutral Spanish, UI labels are just
  "Spanish" / "English"
- Reviews: 10 generated placeholders (one per service), marked as
  placeholder via HTML comments
- Modal qualifying questions:
  1. What marketing service are you interested in? (Google Ads, Facebook,
     Website, Lead Gen, Reputation, Other)
  2. What type of home service business do you run? (Plumbing, HVAC,
     Electrical, Roofing, Landscaping, General Contractor, Other)
  3. Full Name + Phone + Email
- Logo: existing `images/logo-light-backgrounds.png` and
  `images/logo-dark-backgrounds.png`
- Favicon: existing `images/favicon-light-background.png` and
  `images/favicon-dark-background.png`
- Phone: 602-829-0009; Email: mgarcia4@gmail.com; Domain: fireflyrise.com

---

## Standing rules (still in force)

These reflect the SKILL plus Mike's overriding directives:

- **No pricing anywhere.** Verified with `scripts/scan_pricing.py`.
- **Phone only inside `tel:` button links.** Email never on main pages.
  Both allowed in plaintext on legal pages only (per SKILL exception).
  Verified with `scripts/scan_contact.py`.
- **H1 = SEO title content (minus brand).** Title keeps brand for SEO;
  H1 stays clean on-page.
- **Clean URLs (`/slug/`).** No `.html` in any URL.
- **Container max-width: 1200px.** Paragraphs use full container width.
- **Hero `.hero-content` padding: 20px.**
- **Nav has logo only — no business-name text next to it** (Mike's
  override of the SKILL spec; the logo image already contains the name).
- **Footer minimal:** logo + business name + two CTA buttons + copyright.
  No tagline, no service links, no legal links in the footer (those are
  in the nav dropdowns).
- **Language toggle:** plain text link with fa-language icon, sits above
  the `<h1>` on every page (hero on regular pages, top of content block
  on legal/404). White on dark, dark on light, primary color + 110% scale
  on hover.
- **Favicon:** single `<link id="favicon">` + JS `matchMedia` swap. No
  `media="(prefers-color-scheme:...)"` (Chrome ignores it).

---

## Verification scripts

In `scripts/`:
- `scan_pricing.py` — fails if any pricing language slips into the HTML
- `scan_contact.py` — fails if plaintext phone/email appears on non-legal
  pages
- `check_refs.py` — verifies all internal `href` and `src` references
  resolve to actual files
- `validate_env.py` — confirms `.env` has a working `GEMINI_API_KEY`

Run before pushing:
```
python scripts/build_site.py
python scripts/scan_pricing.py
python scripts/scan_contact.py
python scripts/check_refs.py
```

---

## Files / paths reference

```
fireflyrise.github.io/
├── index.html                                   ← English home, served at /
├── 404.html                                     ← served by host on 404
├── CNAME                                        ← fireflyrise.com
├── sitemap.xml                                  ← generated
├── robots.txt                                   ← generated
├── .gitignore                                   ← .env, settings.local.json, worktrees
├── .env                                         ← GEMINI_API_KEY, PABBLY_CONNECT_WEBHOOK (gitignored)
├── SKILL.md                                     ← the build spec
├── convo.md                                     ← THIS file
├── css/styles.css                               ← all site styles
├── js/main.js                                   ← favicon swap, modal, hamburger, FAQ accordion, phone formatter
├── images/                                      ← logos, favicons, 35 generated WebPs
├── references/                                  ← SKILL author's reference files
├── scripts/
│   ├── build_site.py                            ← main page generator
│   ├── site_data.py                             ← business identity + services + reviews
│   ├── faqs_data.py                             ← FAQs per page (EN+ES)
│   ├── generate_images.py                       ← Gemini image generation
│   ├── images_manifest.json                     ← image prompts + filenames
│   ├── validate_env.py                          ← API key validator
│   ├── scan_pricing.py                          ← pricing-leak scanner
│   ├── scan_contact.py                          ← plaintext phone/email scanner
│   └── check_refs.py                            ← internal link validator
├── [10 EN service slugs]/index.html             ← e.g. google-ads-management/index.html
├── [10 ES service slugs]/index.html             ← e.g. administracion-de-google-ads/index.html
├── marketing-digital-para-servicios-del-hogar/  ← Spanish homepage folder
│   └── index.html
├── privacy-policy/index.html
├── terms-and-conditions/index.html
├── politica-de-privacidad/index.html
└── terminos-y-condiciones/index.html
```

---

## How to update this log going forward

After every meaningful change that gets committed:
1. Add a new dated entry at the top of the **Build log** section
2. Format: `### YYYY-MM-DD — Short description (commit \`hash\`)`
3. Two short blocks: **What:** and **Why:**
4. If the change creates a new standing rule, add it to **Standing rules**
5. If it's an experiment that might be reverted, note that explicitly
