# Animated carousels

AWA's default carousel is static (PNG per slide + PDF). Make an animated one when it's asked for, or when motion clearly helps the idea (a list that builds, a reveal) and you say why.

Each animated slide is its own 1080 × 1350 MP4 (about 6 s) so it plays as people swipe to it. Instagram accepts mixed photo and video slides at 4:5; LinkedIn doesn't play video in document carousels, so the same slides are also exported as PNG stills and a PDF.

## Size rule
Every slide MP4 is exactly the same size as its PNG: 1080 × 1350, square pixels. `make_carousel.py --video` checks this on every slide and stops if they differ.

## Build
1. Start from `templates/carousel-animated-cover.html`, `carousel-animated-point.html` and `carousel-animated-cta.html` (one HTML per slide: 01.html, 02.html, ...).
2. Use the motion utilities in `_base.css`, each with a start time: `class="a-rise" style="--d:.4s"`. Entrances: `a-rise`, `a-slam`, `a-pop`, `a-left`, `a-right`, `a-fade`, `a-grow`, `a-growy`, `a-draw`, `a-strike`, `a-out`, `a-shake`. Ambient: `a-drift`, `a-float`, `a-nudge`, `a-pulse`.
3. Timing: text in by ~0.8 s, the visual builds from ~1 s, everything settled by ~3 s, then ambient motion (6 s default via `<meta name="reel-duration">`). The end state must look finished because Instagram loops.
4. Cover rule: on slide 1 the headline and hero are visible at frame 0 (Instagram uses it as the thumbnail).
5. Sound: `<meta name="reel-sfx">` cues per slide (pop, tick, thud, whoosh, ding). No music bed per slide; add one track to the whole carousel in the Instagram app instead.
6. `<meta name="still-time">` (default 4.0 s) is the moment the PNG still captures.

## Render and check
```bash
python3 scripts/make_carousel.py slides/ out/carousel-name.pdf --video
```
Pull frames from each MP4 (frame 0, mid-entrance, settled) with `ffmpeg -ss <t> -i slide.mp4 -frames:v 1 f.png`. Confirm frame 0 of the cover reads on its own and nothing overlaps mid-motion.
