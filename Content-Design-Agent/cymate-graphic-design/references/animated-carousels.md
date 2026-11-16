# Animated carousels (default for every Cymate carousel)

Every carousel ships as animated slides: each slide is its own 1080 × 1350 MP4 (about 6 s) so it plays as people swipe to it. Instagram carousels accept mixed photo and video slides at 4:5, so the MP4s upload straight into one carousel post. LinkedIn doesn't play video in document carousels, so the same slides are also exported as PNG stills and a PDF.

## Size rule
Every slide MP4 is exactly the same size as its PNG: **1080 × 1350 (4:5), square pixels**, so photo and video slides line up perfectly in one Instagram carousel. `make_carousel.py --video` checks this on every slide and stops if they differ. Never export carousel videos at 1080 × 1920 or 1080 × 1080.

## Build
1. Start from `templates/carousel-animated-cover.html`, `carousel-animated-point.html` and `carousel-animated-cta.html` (one HTML per slide: 01.html, 02.html, ...).
2. Use the motion utilities in `_base.css`, each with a start time: `class="a-rise" style="--d:.4s"`.
   Entrances: `a-rise`, `a-slam`, `a-pop`, `a-left`, `a-right`, `a-fade`, `a-grow` (bars, rules), `a-growy` (columns), `a-draw` (SVG lines, set `--len`), `a-strike`, `a-out` (swap one chip for another), `a-shake`.
   Ambient loops: `a-drift` (glow), `a-float`, `a-nudge` (swipe arrow), `a-pulse`.
3. Timing per slide: text in by ~0.8 s, the visual builds from ~1 s, everything settled by ~3 s, then ambient motion until the end (6 s default via `<meta name="reel-duration">`). Instagram loops the video, so the end state must look finished.
4. **Cover rule**: on slide 1 the headline and hero visual are visible at frame 0 (Instagram uses the first frame as the thumbnail). Animate only secondary details there.
5. Sound: `<meta name="reel-sfx">` cues per slide (pop, tick, thud, whoosh, ding…) for the motion. No music bed per slide: a bed restarts on every swipe. Add one track to the whole carousel in the Instagram app instead. Use `--music` only if asked.
6. `<meta name="still-time">` (default 4.0 s) is the moment the PNG still captures; set it after everything has landed.

## Render
```bash
python3 scripts/make_carousel.py slides/ out/carousel-name.pdf --video
```
Outputs per slide `carousel-name-01.mp4` + `carousel-name-01.png`, and `carousel-name.pdf`. Six slides take a few minutes.

## Check
View the stills as a contact sheet, then pull frames from each MP4 (frame 0, mid-entrance, settled) with `ffmpeg -ss <t> -i slide.mp4 -frames:v 1 f.png`. Confirm frame 0 of the cover reads on its own, nothing overlaps mid-motion, and every visible motion has a sound cue.

## Delivery
The slide MP4s in order (Instagram), the PNGs and PDF (LinkedIn), caption, alt text, and a note to add one music track in-app if wanted.

## Format: seamless ribbon carousel
One long stretched word ("REPLIEEEEE…ES", "We’re finallyyyy…", "BOOKEDDDD…") runs across every slide on a single path, so each swipe continues the last. The mascot rides the front of the word, tilting with the waves and revealing the letters; small tags pop up as it passes, and the last slide lands the payoff (calendar, announcement, offer). Example: CR04. Reference: Pinterest stretched-word vehicle carousels.
- Generator: `templates/ribbon-carousel/gen_ribbon.py` (path, word, drive timing, tags and payoff are all set at the top and bottom of the file). It writes one HTML per slide that shares the same global path, so the still panorama joins perfectly.
- Off-white `cm paper` background, orange gradient letters with a soft drop shadow, wordmark-dark top-left and a page counter top-right; social bar or CTA pill only on the last slide.
- Keep the waves gentle and the path moving left to right only; start the word at least 96 px inside slide 1; slide 1 shows headline, first letters and mascot at frame 0.
- Sound: a whoosh as the mascot enters each slide, a pop per tag, a thud and a ding on the payoff.
- Rendering is heavier than normal slides (about a minute per slide). If a batch times out, render each slide with `make_reel.py ... --width 1080 --height 1350 --no-music` and the stills with `render.py`, then join the PNGs into the PDF.
- Check: stitch the five stills side by side to confirm the ribbon is continuous, then pull frames from every MP4 to confirm the mascot sits on the reveal edge.
