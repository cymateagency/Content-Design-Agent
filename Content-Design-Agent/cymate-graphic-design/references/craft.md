# Craft: make it look designed in Photoshop, not generated

Cymate posts should look like a senior designer built them by hand in Photoshop: deliberate, physical, finished. Generated-looking work is the fastest way to lose an enterprise buyer’s trust. This file is the standard; `scripts/qa.py` and `scripts/finish.py` enforce the mechanical parts automatically.

## 1. Think in layers, like a PSD
Build every poster as a stack, back to front, and name the layers in your head:
1. **Background** (near-black + ember glow, burnt orange or paper) with one texture.
2. **Atmosphere**: a light source (orange glow behind the hero), light streaks, out-of-focus shapes.
3. **Hero object** (card, device, prop, photo) with its **shadow layers** underneath it.
4. **Type**: headline, sub, labels.
5. **Overlay details**: callouts, tags, stickers, annotations that sit *on top* and overlap the hero a little.
6. **Brand frame**: header, social bar.
7. **Finish** (adjustment layers): curves, split tone, bloom, vignette, grain. Done by `finish.py` on every render.
Overlap between layers (a tag crossing a card edge, a prop in front of a headline’s descender) is what makes a composition feel handmade. Use it on purpose and mark deliberate text overlaps with `data-overlap`.

## 2. One light, consistent shadows
- Pick one key light per poster (default: top-left, warm). Every highlight, gradient and shadow agrees with it.
- Every floating object gets **two shadows**: a tight, dark contact shadow (blur 8–16 px, offset 6–12 px) and a big soft ambient shadow (blur 50–100 px, offset 30–60 px, 35–60% black). One flat drop shadow looks fake.
- Lit edges: a 1 px inner highlight on the top edge of cards, keys and glass (`inset 0 1px 0 rgba(255,255,255,.x)`).
- Objects closer to the camera are larger, sharper and cast longer shadows; things behind get a little blur (depth of field) and lower contrast.

## 3. Real materials
- **Glass**: backdrop blur, 6–16% white fill, bright top edge, faint border, content behind visibly blurred.
- **Plastic / keys**: two-tone body (darker sides), inner bevel, soft highlight, contact shadow.
- **Paper / labels**: warm off-white (never pure #FFF), slight rotation, a crisp shadow on one side.
- **Screens**: real UI conventions (status bar, timestamps, avatars, realistic names), slightly smaller text than you’d think, never lorem ipsum.
- **Photos**: use real photography whenever it fits (team shots, office, desk, stock at 20–30%). A real photo instantly reads as human-made. Grade it to the brand (neutral shadows, warm highlights, no blue cast) so it sits in the scene.

## 4. Typography a designer would sign off on
- Display sizes get tighter tracking (−1 to −3 px) and tighter leading (0.9–1.05); body copy gets 1.35–1.5 leading.
- Curly quotes and apostrophes (’ “ ”), never straight ones; no em dashes (Cymate voice); no double spaces.
- No widows: never a single word alone on the last line of a headline. Use `<br>` to break lines by meaning, not by accident.
- Mix weights for rhythm (light setup, heavy payoff) but at most two families per post (Poppins + Inter; Plex Mono for micro labels).
- Optical alignment: text blocks share exact left edges; big type may hang 4–8 px left of the margin so it *looks* aligned. A 1–8 px accidental offset is the most common “sloppy” tell; QA flags it.
- Minimum 18 px for anything meant to be read (UI metadata in mockups may be smaller; mark it `data-small`).

## 5. Grid and spacing
- Margins 96 px left/right on 1080 wide; content never closer than 56 px to any edge.
- Spacing from one scale only: 8, 12, 16, 24, 32, 48, 64, 96. Equal gaps between equal things.
- Align to something: every element’s edge or centre lines up with another element or the margin.

## 6. Avoid the AI tells
These patterns make a post look generated. Don’t use them unless the concept needs it:
- Everything perfectly centred and symmetrical; every corner the same radius; every card the same size.
- Glowing blobs on every corner, neon gradients everywhere, “aurora” backgrounds with no light logic.
- Sparkle/✨ emoji, rocket emoji, generic 3D blobs, isometric clip-art, stock “robot hand”.
- Vague copy (“Unlock growth”, “Supercharge your pipeline”), fake-looking UI text, random numbers.
- Plastic-smooth gradients with banding (the grain/dither in `finish.py` prevents this).
- Shadows that point in different directions; objects floating with no shadow at all.
- Perfect hand-drawn effects (marker text must wobble, lines must jitter, as in P10).

## 7. Finish pass (automatic)
`render.py` renders at 2× and downsamples with Lanczos (clean edges like a Photoshop export), then runs `finish.py`: curves, split tone, bloom, vignette, smart sharpen and luminance-aware grain. Use `--finish 0.7` for very clean UI-heavy posts, `--finish 1.3` for moodier photo posts, `--raw` only to debug. Reels and animated carousels get matching temporal grain and vignette in `make_reel.py`.

## 8. Accuracy (perfect means correct)
Before delivering, every item must be true:
- Zero WARN lines from `render.py`, or each remaining one is confirmed deliberate (name it in your head: a fictional company name, an intentional overlap).
- Spelling and grammar checked by `qa.py` and then by eye, word by word, including small UI text.
- Handles and links exactly: @cymate.io (IG), @CymateLLC (YouTube), Cymate (LinkedIn), cymate.io.
- Facts: no invented stats, results, client names or quotes. Jokes are clearly jokes. Technical claims (SPF, DKIM, DMARC, warmup, volume) are correct.
- The image and the caption say the same thing (same numbers, same names, same CTA).
- Dates, days and seasonal references are right for the posting date.
- Sizes: 1080 × 1350 for feed posts and carousel slides (PNG and MP4 identical).
