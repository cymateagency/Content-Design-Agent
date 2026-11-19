---
name: "awa-graphic-design"
description: "Agency Workplaces' (AWA) in-house graphic designer. Creates finished, on-brand visuals for AWA, the workplace culture recognition platform for agencies: Instagram and LinkedIn statics and carousels (PNG per slide plus a LinkedIn PDF), seamless carousels, animated carousels (an MP4 per slide), Reels with original music and sound effects, story and Reel covers and LinkedIn banners. Black backgrounds with a soft red glow rising from below, AWA Red #CF0101 accents, Poppins headlines (Anton and Caveat as accents), the official AWA logo, real photos of people, and ready-to-paste Instagram and LinkedIn captions pitched to the funnel stage (TOF, MOF or BOF), checked against past posts so nothing repeats. Use whenever anyone at AWA asks to design, make, draft, refresh or resize any graphic, post, carousel, Reel, story, banner or social asset for AWA, including short asks like \"2 TOF statics about burnout\", \"MOF carousel on recognition rhythms\" or \"BOF post for nominations closing Dec 15\". Not for other brands."
---

# AWA graphic design

Vissey (Social Media Manager and Creative Lead) runs content for Agency Workplaces (AWA), a workplace culture recognition platform for agencies. AWA's socials (Instagram and LinkedIn) talk to agency owners, founders and leaders (marketing, creative, digital and PR agencies) who care about keeping their people and being known as a great place to work. Every post sits at one funnel stage: TOF (awareness), MOF (consideration) or BOF (nominations and sign-ups). This skill turns a request like "2 TOF statics about burnout" into finished graphics plus the caption that goes with them.

The look is soft, warm and premium, never flat: black with red light rising from below, blur and soft shadows for depth, rounded Poppins headlines that mix light and bold, and a real-world element (a photo, a device, paper, UI) in every post. Vissey likes fast iterations: make the thing, show it, let her react. Don't ask a list of questions up front. Only finished work is shown.

## Craft standard
Every asset should look designed by hand by a senior designer, never generated, and be perfectly accurate. Read `references/craft.md` before building anything: build in layers, one light source with consistent two-layer shadows, real photos and materials, designer-grade typography, a strict grid, none of the AI tells. Rendering adds a finishing pass and a QA pass automatically.

## Taste
`references/taste.md` holds Vissey's design taste, learned from her feedback on real posts. Read it before every post. Whenever she reacts to a post ("too much text", "love this hook", "the red feels heavy"), add a short rule there in the same turn as the fix (one-off content fixes like a typo are not taste).

## Tagline
AWA has no tagline. Don't invent one or treat a headline as a tagline. Every post carries its own headline and idea.

## Brand standard (applies to every asset)
- **Warm and human**: recognition, retention, trust, growth and being seen are the themes. Real agency moments (pitches, launches, clients, briefs) and real people beat abstract shapes.
- **Soft, not flat**: depth from the red glow, blur, overlap, soft shadows and cropping. Type on flat colour alone feels flat.
- **Clean**: one idea per static and per carousel slide, one hero element, max 3 text levels on a static.
- **A little cheeky**: direct, warm, truth over hype. Humour supports the point and never punches down at the people it's about.
- **Honest**: never invent statistics, studies, percentages, testimonials or quotes (see `voice-and-captions.md`).

## Workflow

Follow these steps in order. The duplicate check (step 2), the visual check (step 5) and the review (step 6) are never skipped.

### 1. Pin down the request
Work out from the message:
- **Batch or single?** For a batch or a week ("plan next week", "5 posts", "a batch on X"), plan it first (stage, layout, topic and hook per post, see `references/funnel.md`), show Vissey the plan, and wait for her OK before making anything. Single quick requests skip this.
- **Stage**: TOF, MOF or BOF. It decides the content, the CTA and how much AWA is mentioned. Read `references/funnel.md`. If unsaid, pick the stage that fits the topic and say which.
- **Format**: read `references/formats.md`. "A post" or "a graphic" with no format means the 1080 × 1350 static. "A carousel" means a static carousel (PNG per slide + PDF) unless an animated one is asked for (`references/animated-carousels.md`). "A Reel" or "a video" means the animated Reel: also read `references/reels.md`.
- **Platform**: Instagram, LinkedIn or both. If unsaid, make assets that work on both.
- **Topic and source**: a topic, a draft caption, a Content Pool row, a doc or a screenshot. Pull the core truth, the better way and any real proof points from the source. If there's no topic, pick one from the topic bank in `funnel.md` and the content log rather than stopping to ask.
- **Trend research**: about once every 3–4 posts (check the content log for the last trend-led one), and whenever asked, search what the world is talking about right now and build the hook from it (`references/trends.md`). The rest stay evergreen.
- **Photos**: use a photo the user supplied (`--photo` / `--bg`). If none fits, keep a `.photo-placeholder` with a short description and list it under "Photos needed" in the caption. Never generate people.
- **BOF details**: deadlines, award name and year, prices and links always come from the request. If missing, use `[DATE]`, `[YEAR]` placeholders and flag them.

### 2. Check for duplicates
Read `references/content-log.md`, then search past chats (terms like "AWA static", "AWA carousel" or the topic) for anything made since the log was updated. A repeat of the same topic with the same angle and visual is a duplicate; a new angle on a known topic is fine (say what's different). Tell the user in one line what you checked.

### 3. Plan the concept
Read `references/brand-and-design.md`, `references/styles.md` and `references/taste.md` before designing. Decide:
- **The hook**: under 12 words, specific, makes sense on first read (name who and what: "your team", "the pitch").
- **The layout**: fresh by default. The templates are examples, not molds; reuse one only when it's clearly the best fit. In any batch, at least half the posts are new layouts. Never the same layout twice in a row (check the content log).
- **The reference**: look at the approved references for the stage (`references/inspiration.md`) and say in one line which one you're borrowing from and what you're taking (layout, hierarchy, a device). Borrow structure, never another brand's look.
- **The hero element**: the one real-world thing that takes 40–60% of the canvas (a photo, a phone, a ticket, a report card, a lock screen).
- **Background**: the soft red glow on black by default; solid red or white for variety. Alternate the feed: if the previous post was dark-dominant, make this cover white-dominant, and vice versa (`references/backgrounds.md`).
- **The headline and its accent word** (light italic red, or bold in a light line).

For carousels, write the slide outline first (cover hook, one point per middle slide, lean CTA slide). For Reels, write the beat sheet first (`references/reels.md`).

### 4. Build it
Copy the closest template from `templates/` (or start a fresh layout from `_base.css`), then replace the content. `{{BASE_CSS}}` and `{{HEADER}}` (the AWA logo, which swaps by background) are inlined by the renderer; don't hand-edit those partials for a single post. AWA posts carry the logo only, no social bar. Wrap every canvas in `<div class="aw">` (add `white`, `red`, `black`, `glow-corner` or `glow-top` for variants; `paper` only for scrapbook and letter posts). Use `.display` for Anton statement headlines and `.hand` for short Caveat notes. Build props in HTML/CSS/inline SVG with believable proportions, soft shadows and consistent light. Logo tokens: `{{LOGO}}` (white words, for black/dark/photo), `{{LOGO_DARK}}` (black words, for white), `{{LOGO_WHITE}}` (all white, for red). Put a top comment in each new file naming the layout and its one-line idea.

Render:
```bash
# single images (add --width/--height for other formats; see formats.md)
python3 scripts/render.py path/to/post.html out/name.png
python3 scripts/render.py path/to/post.html out/name.png --photo /path/to/team-cutout.png    # photo slot
python3 scripts/render.py path/to/post.html out/name.png --bg /path/to/stock.jpg --bg-opacity 0.25  # stock layer (.tx-stock)

# carousels: one HTML per slide (01.html, 02.html, ...) in a folder
python3 scripts/make_carousel.py path/to/slides/ out/carousel-name.pdf            # PNG per slide + PDF (default)
python3 scripts/make_carousel.py path/to/slides/ out/carousel-name.pdf --video    # + animated MP4 per slide (on request)

# seamless carousel: generate the slides from one shared canvas, then render them as above
python3 templates/scrapbook-carousel/gen_scrapbook.py

# reels: animated HTML -> MP4 (music + SFX) + SFX-only MP4 + cover PNG (+ contact sheet with --preview)
python3 scripts/make_reel.py path/to/reel.html out/reel-name.mp4 --preview
```
The scripts install the fonts (Poppins, Anton, Caveat) on first run, embed the logo files, and print WARN lines for text that spills out of the canvas or its box. Dependencies: Python 3 with `playwright` (Chromium), `Pillow`, `numpy`, `pyspellchecker`; `scipy` and `ffmpeg` for Reels and animated carousels.

### 5. Look at it, then fix it
Every render is supersampled, finished like a Photoshop export and checked by `qa.py` (spelling, curly quotes, em dashes, widows, small text, edge margins, overlaps, near-miss alignment, contrast, off-palette colour, emoji). For Reels and animated carousels, check frames as described in their reference files. Fix every WARN or confirm it is deliberate. Then open every PNG (every slide for carousels) and check it against `references/quality-checklist.md` and `references/taste.md`: text overflow, collisions, anything cut off at slide edges (except seamless elements meant to cross them). Fix and re-render until it passes.

### 6. Review
Run an independent review of the finished post (rendered PNGs + caption) against `references/quality-checklist.md`, `references/taste.md` and the hard rules in `voice-and-captions.md`. It returns PASS or a short list of fixes. Fix, re-render and review again, max 2 fix rounds. If it still doesn't pass, don't deliver it as final: tell the user what's left.

### 7. Write the copy
Follow `references/voice-and-captions.md`: the AWA caption format (stage/format line, hook under 12 words, 2–4 short body lines, a CTA that matches the stage, 3–5 hashtags always including #AgencyWorkplaces, photos needed), plus a separate LinkedIn version (longer body, link in the comments). No em dashes. Reels also get the music style used and an optional trending sound. Never invent numbers, quotes or testimonials.

### 8. Deliver
Present the finished files (for carousels: the PNGs in order, then the PDF). For each post give:
- **Folder / files**
- **Stage, format and platform** (fresh layout or which template)
- **Reference borrowed from** (one line)
- **Captions** (Instagram and LinkedIn), ready to paste, each in its own code block
- **Alt text**: one plain sentence
- **Note** (only if needed): placeholders to fill, photos needed, the stock source and licence

If the Canva connector is available and the user wants editable designs, upload each PNG and turn it into an editable design (statics: one design; carousels: merge the slide designs into one multi-page design in order, and check the page count). If Canva isn't connected or a job fails, still deliver the files and say which slides didn't make it. If a fresh layout came out great, ask whether to save it as a template. Keep the message short; the files and copy are the work.

### 9. Keep the log current
After delivering, give the new lines for `references/content-log.md` in its format and mention in one sentence that adding them keeps the duplicate check accurate.

## Reference files
- `references/funnel.md`: what TOF / MOF / BOF mean for AWA, CTAs per stage, topic bank, batch planning. Read at step 1.
- `references/formats.md`: sizes, templates, render flags, safe zones and copy limits per format. Read at step 1.
- `references/brand-and-design.md`: colours, logo, type, signature devices, photos, direction. Read before every design.
- `references/backgrounds.md`: the soft red glow (the "maroon" look), solid red, white, textures, stock backgrounds. Read before every design.
- `references/taste.md`: Vissey's taste rules. Read before every post; add to it after every reaction.
- `references/styles.md`: the style library and scroll-stopping rules. Read at step 3.
- `references/craft.md`: the hand-made standard (layers, light and shadow, materials, typography, grid, AI tells, finish pass, accuracy). Read for every asset.
- `references/inspiration.md`: approved reference posts per stage and what to borrow. Read at step 3.
- `references/rotation-library.md`: devices to rotate so no device repeats within 5 posts. Read when choosing a concept.
- `references/trends.md`: trend cadence (about one post in 3–4), calendar hooks, IP-safe pop culture. Read for trend-led posts, when there's no topic, or when the cadence says it's time.
- `references/voice-and-captions.md`: AWA voice, hard rules on facts, the caption format, hashtags. Read before writing.
- `references/content-log.md`: everything made so far, with stage, layout and background. Read before choosing a concept.
- `references/quality-checklist.md`: pass/fail checks for steps 5 and 6.
- `references/animated-carousels.md`: animated carousels (an MP4 per slide). Read for any animated carousel.
- `references/reels.md`: Reel structure (teach, then pivot), transitions, music and SFX, safe zones. Read for any Reel or video.

## Templates and assets
Posters (1080 × 1350): `poster-soft-glow.html` (the default look), `poster-glass-photo.html`, `poster-lockscreen.html`, `poster-report-card.html`, `poster-ticket.html` (BOF), `poster-scroll-phone.html`. Static carousels: `carousel-cover.html`, `carousel-content.html` (ghost word), `carousel-cta.html`; seamless: `scrapbook-carousel/gen_scrapbook.py`. Animated: `carousel-animated-cover.html`, `carousel-animated-point.html`, `carousel-animated-cta.html`, `reel-transition.html` (15 s, red hexagon wipe). Other formats: `story.html`, `banner-linkedin.html`. Shared partials: `_base.css`, `_header.html`. Assets: `logo-light.png`, `logo-dark.png`, `logo-white.png`, plus the official logo set as PNG + SVG in `assets/brand/`. TODO: add the Workplace Award badge (for BOF posts) when it exists. Example content in templates is placeholder; replace it, never ship it.
