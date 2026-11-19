# Craft: make it look designed by hand, not generated

AWA posts should look like a senior designer built them: deliberate, physical, finished. `scripts/qa.py` and `scripts/finish.py` enforce the mechanical parts automatically.

## 1. Think in layers
Build every poster as a stack, back to front:
1. **Background**: black with the red glow (or solid red, or white), with at most one texture.
2. **Atmosphere**: the light source (red glow behind the hero), blurred shapes, halos.
3. **Hero object** (photo, phone, ticket, card, paper) with its **shadow layers** underneath.
4. **Type**: headline, subline, labels.
5. **Overlay details**: pills, tags, notes that sit on top and overlap the hero a little.
6. **Brand frame**: the logo.
7. **Finish**: curves, split tone, bloom, vignette, grain. Done by `finish.py` on every render.
Overlap between layers is what makes a composition feel handmade. Use it on purpose and mark deliberate text overlaps with `data-overlap`.

## 2. One light, consistent shadows
- One key light per poster: by default the red glow from below. Highlights and shadows agree with it.
- Every floating object gets two shadows: a tight contact shadow (blur 8–24 px, offset 6–14 px) and a big soft ambient one (blur 50–100 px, offset 30–60 px, 35–60% black).
- Lit edges: a 1 px inner highlight on the top edge of cards and glass.
- Closer objects are larger, sharper and cast longer shadows; things behind get a little blur (like the backlit crowd in CP-002).

## 3. Real materials
- **Glass**: backdrop blur, 12–16% white fill, bright top edge, 30–40% white border.
- **Paper / cards**: white, or Paper `#F6F1EA` in scrapbook and letter posts; slight rotation, a crisp shadow on one side.
- **Screens**: real UI conventions (status bar, times, avatars, invented first names), never lorem ipsum, no real app colours.
- **Photos**: real photography whenever it fits. Grade it into the scene so no off-palette colour pulls focus.

## 4. Typography
- Poppins by default; Anton (`.display`) for one statement headline at most; Caveat (`.hand`) for short notes only. Poppins display sizes get tight tracking (−0.04 to −0.05 em) and tight leading (0.95–1.05); body copy 1.25–1.45.
- Curly quotes and apostrophes (’ “ ”), never straight ones; no em dashes (AWA voice); no double spaces.
- No widows: never a single word alone on the last line of a headline. Break lines by meaning with `<br>`.
- Mix weights for rhythm: light setup, bold payoff, one light-italic red accent word.
- Text blocks share exact left edges. A 1–8 px accidental offset reads as sloppy; QA flags it.
- Minimum 18 px for anything meant to be read (mock UI text may be smaller; mark it `data-small`).

## 5. Grid and spacing
- Margins 96 px left/right on 1080 wide; text never closer than 56 px to any edge (mark deliberate edge-crossers `data-edge`).
- Spacing from one scale: 8, 12, 16, 24, 32, 48, 64, 96. Equal gaps between equal things.
- Headline, subline and CTA sit as one tight block.

## 6. Avoid the AI tells
- Everything centred and symmetrical; every card the same size and radius.
- Glow blobs in every corner with no light logic; neon gradients.
- Emoji, sparkles, generic 3D blobs, isometric clip-art, faceless stock figures.
- Vague copy ("Unlock your culture"), fake-looking UI text, invented numbers.
- Flat banded gradients (the grain in `finish.py` prevents this); objects floating with no shadow.

## 7. Finish pass (automatic)
`render.py` renders at 2× and downsamples with Lanczos, then runs `finish.py`: curves, split tone, bloom (bright and red areas glow softly), vignette, smart sharpen and grain. Use `--finish 0.7` for very clean UI posts, `--finish 1.3` for moodier photo posts, `--raw` only to debug.

## 8. Accuracy (perfect means correct)
- Zero WARN lines from `render.py`, or each one is confirmed deliberate.
- Spelling and grammar checked by `qa.py` and then by eye, word by word, including small UI text.
- Website exactly: agencyworkplaces.com. No social handles on designs.
- Facts: no invented stats, quotes, testimonials or client names. Award names, years, deadlines and prices only from the request.
- The image and the caption say the same thing (same CTA, same names, same dates).
- Dates, days and seasonal references are right for the posting date.
- Sizes: 1080 × 1350 for feed posts and carousel slides.
