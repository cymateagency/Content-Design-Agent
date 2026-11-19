# Formats

If a request just says "a post" or "a graphic", make the 1080 × 1350 portrait static (works on Instagram and LinkedIn). Platform specs change; if a crop looks wrong or the user mentions one, check current guidance with a web search.

| Format | Size (px) | Template | Render | Delivered as | Copy |
|---|---|---|---|---|---|
| Static post (IG + LinkedIn) | 1080 × 1350 | a fresh layout on `_base.css`, or a `poster-*.html` | `render.py` (+ `--photo` / `--bg`) | PNG | Caption |
| Carousel (static, default) | 1080 × 1350 per slide, 4–7 slides | `carousel-cover.html`, `carousel-content.html`, `carousel-cta.html` (one HTML per slide: 01.html, 02.html, ...) | `make_carousel.py slides/ out/name.pdf` | PNG per slide + PDF | Caption |
| Seamless carousel | 1080 × 1350 per slide, one shared canvas | `scrapbook-carousel/gen_scrapbook.py` | generator, then `make_carousel.py` | PNG per slide + PDF | Caption |
| Animated carousel (on request) | 1080 × 1350 per slide, ~6 s each | `carousel-animated-*.html` (see `animated-carousels.md`) | `make_carousel.py --video` | Instagram: MP4 per slide. LinkedIn: PNG stills + PDF | Caption |
| Square post | 1080 × 1080 | adapt a poster | `--width 1080 --height 1080` | PNG | Caption |
| Story / Reel cover | 1080 × 1920 | `story.html` | `--width 1080 --height 1920` | PNG | Short caption or none |
| Reel | 1080 × 1920, 10–30 s, 30 fps | `reel-transition.html` (see `reels.md`) | `make_reel.py` (+ `--bg-video` / `--bg`) | MP4 (music + SFX) + SFX-only MP4 + cover PNG | Caption + music style + suggested sound |
| LinkedIn personal banner | 1584 × 396 | `banner-linkedin.html` | `--width 1584 --height 396` | PNG | Alt text only |
| LinkedIn company cover | 1128 × 191 | adapt `banner-linkedin.html` | `--width 1128 --height 191` | PNG | Alt text only |

## Templates (examples, not molds)
Fresh layouts are the default; reuse a template only when it's clearly the best fit, and keep at least half of any batch new. Each template has a comment at the top with its idea and SLOTS limits. They came from AWA's approved formats in the awa-posts project.

| Template | Type | Best for | Idea |
|---|---|---|---|
| `poster-soft-glow` | static | TOF, MOF, BOF (swap the pill) | The default look (CP-002): big rounded headline, light-italic red accent, one subline, one pill, a real person or crowd rising out of the red glow |
| `poster-glass-photo` | static | TOF, MOF, BOF | Full photo, frosted panel, light + bold headline, one pill |
| `poster-lockscreen` | static | TOF | Fake lock-screen notifications tell a tiny story, one-line payoff |
| `poster-report-card` | static | TOF | Humour: perks get A's, what matters gets F's |
| `poster-ticket` | static | BOF | Golden-ticket metaphor for nominations or deadlines |
| `poster-scroll-phone` | static | TOF (MOF via caption) | First-impressions hook, a phone mid-scroll with a countdown ring, glass tip card with the fix |
| ghost-word carousel (`carousel-cover` / `-content` / `-cta`) | carousel, 5 slides | MOF | Cover, 3 lessons with a giant outlined vertical ghost word, lean CTA |
| `scrapbook-carousel` | seamless carousel, 5 slides | TOF | One wide canvas: torn paper, polaroid and a note crossing slide edges |
| TODO: award explainer (curves) | carousel, 6 slides | MOF (BOF with a hard CTA) | Saved in awa-posts as `carousel-award-explainer-curves` (from CP-012) but not ported yet; port it after the award facts are confirmed |

## Ideas to build next (from the awa-posts inspo round)
- resignation letter (TOF): a letter with excuses crossed out and the real reason circled
- poll (MOF): checkbox poll, "vote in the comments"
- mirror (MOF): "what leaders say" vs "what teams hear" split
- pennant (TOF): big headline with a white pennant ribbon on one word
- connecting line (MOF): a red line that snakes across slides linking steps
- big stat (MOF): big number slides with an oversized outline icon (real data only)
- spotlight (MOF): leader photo with red name bar and diamond pattern

## Format rules
**Every canvas**: 1080 × 1350 for feed posts and carousel slides, exactly. AWA colours and fonts only (`brand-and-design.md`). One idea per static or slide, a clear hierarchy, max 3 text levels on a static, a CTA that fits the stage.

**Carousels**
- Slide 1 (cover): hook + one subline + swipe cue. No body paragraph. It must stop the scroll on its own. Alternate dark/white covers across the feed.
- Middle slides: one point each; heading ≤ 5 words, body ≤ 25 words, page count.
- Last slide: lean. Statement + one CTA + the URL, nothing between them.
- Same background family and frame on every slide.

**Seamless carousels**: objects (paper, photos, notes) cross the slide edges on purpose; text never does. Keep text at least 56 px from every edge on its own slide.

**Story / Reel cover**: keep the top 250 px and bottom 340 px free of text. For Reel covers, keep key text inside the centre 1080 × 1350.

**Banners**: the profile photo covers the bottom-left (personal) and the logo tile covers the left (company). Keep content in the right ~60%.

## Adding a new template
When the user drops a reference and says "make this a format", or says yes to saving a fresh layout: study its structure (hierarchy, what crosses edges, where the CTA sits), not the other brand's look; build `templates/<type>-<name>.html` on `_base.css` with a top comment (style, stage, one-line idea, SLOTS with limits); add it to the table above; render it and show it. Never save one without a yes.
