# Formats

If a request just says "a post" or "a graphic", make the 1080 × 1350 portrait static (works on Instagram and LinkedIn). Platform specs change; if a crop looks wrong or the user mentions one, check current guidance with a web search.

| Format | Size (px) | Template | Render flags | Delivered as | Copy |
|---|---|---|---|---|---|
| Static post (IG + LinkedIn) | 1080 × 1350 | a `poster-*.html` style (see `styles.md`) | none (+ `--photo` / `--bg` when the style uses them) | PNG | Caption (IG or LinkedIn version, or both) |
| Square post | 1080 × 1080 | adapt a `poster-*.html` style (move the social bar up to `bottom:60px`) | `--width 1080 --height 1080` | PNG | Caption |
| Carousel (animated, default) | 1080 × 1350 per slide, 5–8 slides, ~6 s each | `carousel-animated-cover.html`, `carousel-animated-point.html`, `carousel-animated-cta.html` (see `animated-carousels.md`) | `make_carousel.py --video` | Instagram: one MP4 per slide. LinkedIn: PNG stills + PDF. Always give both | Caption |
| Carousel (static, only if asked) | 1080 × 1350 per slide | `carousel-cover.html`, `carousel-content.html`, `carousel-cta.html` | `make_carousel.py` | PNGs + PDF | Caption |
| Story / Reel cover | 1080 × 1920 | `story.html` | `--width 1080 --height 1920` | PNG | Short caption or none |
| YouTube thumbnail | 1280 × 720 | `thumbnail-youtube.html` | `--width 1280 --height 720` (+ `--photo` if Wesley is on it) | PNG | Title options (2–3); descriptions belong to the `cymate-shortform-description` skill |
| Reel (video) | 1080 × 1920, 10–30 s, 30 fps | `reel-transition.html` (see `reels.md`) | `make_reel.py` (+ `--bg-video` / `--bg`) | MP4 + cover PNG | Caption + suggested sound |
| Looping GIF (LinkedIn) | 1080 × 1350, 2–4 s loop, under 5 MB, ≤250 frames | `gif-loop/gen_factory_gif.py` (see `gifs.md`) | `make_gif.py --fps 24 --mp4` | GIF + MP4 + still | LinkedIn caption |
| YouTube channel banner | 2560 × 1440 (16:9), under 6 MB | `banner-youtube.html` (official Champions look: `champions/gen_champions_banner.py`; five more looks in `banner-youtube-variants/gen_variants.py`) | `--width 2560 --height 1440` | PNG + a safe-zone guide PNG | Alt text only |
| LinkedIn personal banner | 1584 × 396 | `banner-linkedin.html` | `--width 1584 --height 396` | PNG | Alt text only |
| LinkedIn company cover | 1128 × 191 | adapt `banner-linkedin.html` | `--width 1128 --height 191` | PNG | Alt text only |

## Format rules
**Carousels**
- Slide 1 (cover): kicker + hook headline + swipe cue. No body paragraph. It must stop the scroll on its own.
- Middle slides: one point each; ghost numeral, kicker ("Step 1", "Mistake 2"), headline, max ~30 words of body, an optional small visual. Update the ghost numeral and progress dots on each slide.
- Last slide: takeaway + one CTA that matches the caption's hard CTA.
- Same background family and frame on every slide; alternate the glow corner for rhythm.

**Story / Reel cover**: keep the top 250 px and bottom 340 px free of text. For Reel covers, keep key text inside the centre 1080 × 1350 so the grid crop still reads.

**YouTube thumbnail**: 2–5 words, huge, readable on a phone. Leave the bottom-right corner empty (video length badge). With Wesley: photo on the right, text in the left 60%.

**YouTube banner**: only the centre 1546 × 423 (x 507–2053, y 508–931) shows on every device; logo, headline and anything essential go there. Desktop shows the full-width 2560 × 423 strip (decorative extras only at the sides), tablets 1855 × 423, TVs the whole canvas (atmosphere only above and below). Text at least ~90 px for headlines (the safe area shrinks to phone width). Always check the mobile crop and deliver a safe-zone guide.

**Banners**: the profile photo covers the bottom-left (personal) and the logo tile covers the left (company). Keep content in the right ~60% / right half.
