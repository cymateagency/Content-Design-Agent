# Looping GIFs (LinkedIn)

Simple illustrated scenes where one or two things loop forever: envelopes riding a conveyor between stations, a belt sliding, lamps blinking, a badge popping. Inspired by ColdIQ's "GTM Factory" GIF (warm, top-down, labelled stations, a CTA pill). First Cymate example: G01 "Inside the Outbound Factory".

## Concept library (rotate these, don't repeat one look)
Research notes (Nov 2026): short 3–6 s seamless "loopers", kinetic typography, animated infographics/UI, metallic finishes, and deliberately imperfect hand-drawn motion at low frame rates are what's working. Lead with the idea, not the logo.
- **Factory / conveyor** (G01–G05, `gen_factory_gif.py`, `gen_factory_variants.py`): stations on a looping belt. Themes: paper, near-black, burnt orange, Champions; layouts: rounded rect, ring, stadium, square.
- **Live inbox feed** (L01, `gen_loop_concepts.py`): a phone inbox where positive replies keep arriving at the top; hold, then slide one row; list duplicated so the end matches the start. 6 s at 20 fps.
- **Kinetic marquee** (L02): two giant Bebas rows sliding opposite ways behind a static message card. Keep it to two rows and render with `--dither none --colors 48` (big moving areas balloon GIF size). 4 s at 15 fps.
- **Reply radar** (L03): a sweep rotating once per loop; blips and labels light up exactly when the sweep passes (negative animation delays keep it periodic). 4 s at 20 fps.
- **Hand-drawn boil** (L04): paper, wobbly ink lines redrawn 3 ways and cycled at 8 fps (`steps(1)`), a paper plane on an ellipse at 12 fps, handwritten words. 3 s at 12 fps, tiny files.
Other ideas to try next: a toggle switch flipping "spam" to "inbox", a pipeline bar filling and resetting, a calendar whose slots fill one by one, an orbit of tool icons around the mascot.

## Specs
- 1080 × 1350 (4:5) for the LinkedIn feed (1080 × 1080 also fine). LinkedIn plays animated GIFs in the feed; keep each file under 5 MB and under 250 frames.
- Loop 2–4 s at 15–24 fps. Every animation must repeat with a period that divides the loop (`<meta name="gif-loop" content="3">`): move objects exactly one slot, slide belts one dash period, blink lamps an exact number of times. Frame 0 = frame N, so there is no jump.
- Flat illustration only: solid fills, 3 px ink outlines, hard offset shadows (`0 8px 0 ink`), paper/cream base. No film grain, no big soft gradients, no photos (they balloon GIF size). `finish.py` is not applied.
- Keep it simple: one moving system plus small secondary loops. Text never moves.
- Brand: paper/cream background, near-black ink, orange accents, official wordmark and mascot. The mono kicker can carry a short label of your choosing (the tagline is optional, not a default). No blue anywhere.

## Build and render
1. Start from `templates/gif-loop/gen_factory_gif.py`, or `gen_factory_variants.py` for themed versions (dark, burnt orange, Champions, paper) and layouts (rounded rectangle, ring, stadium, square) (conveyor loop, six stations, centre card, CTA). Change stations, copy and loop length at the top.
2. `python3 scripts/make_gif.py scene.html out/name.gif --fps 24 --mp4`
   It renders the loop, builds one optimised palette, and steps the width (1080 → 960 → 864 → 720) or the frame rate down if the file goes over 5 MB. `--mp4` also writes a ~9 s MP4 of the same loop, and a `-still.png` is saved for previews.
3. Check: view frames 0, ¼, ½, ¾ of the loop side by side; confirm the moving parts never cover text, and the first and last frames match.

## Delivery
The GIF (LinkedIn), the MP4 (backup / other platforms), the LinkedIn caption, alt text.

## Background variety
Rotate the four themes so the feed doesn't repeat: paper (G01, G05), near-black (G02), burnt orange (G03), Champions charcoal with diagonal streaks and a Bebas title (G04). On dark themes use white text, warm grey descriptions, orange lamps and an orange or white CTA; keep contrast at least 4.5:1 for small text.

## Capture note
All renderers launch Chromium with threaded (compositor) animation disabled. Without that, seeked frames can show a different moment than the one requested (a constant ~0.6 s offset), which skips the start of entrance animations in reels and carousels.
