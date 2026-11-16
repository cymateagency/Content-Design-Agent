# Inspiration board (approved look, November 2026)

The team picked these seven posts as the direction for Cymate's look. Borrow their **touch** (finish, composition, a signature move), never their layout, copy or subject. Each Cymate post keeps its own DNA: the wordmark and mascot header, the orange signature gradient, Poppins/Inter type, the social bar, and black with a faint blue haze as the default. Not every post needs one of these looks; mix them in with the existing styles.

Files are in `assets/inspiration/`. View the matching one before building a post in that direction.

| # | File | The touch to borrow | Cymate version (template) |
|---|---|---|---|
| 1 | `01-glass-steps-orange-light.jpg` | Numbered frosted-glass cards fanned diagonally, alternating light and dark glass, over warm orange light that flows like silk. Thin orbit line with one orange dot. Light-weight headline with one bold orange word. Tiny tracked kicker with a short orange rule. | `poster-glass-steps.html`: process, services, "how we run it", 3-4 step frameworks |
| 2 | `02-spec-callouts-product-sheet.jpg` | Treat one object like a product launch: bounding box with square handles, technical callout lines with tiny uppercase notes, small corner words, a ruled spec table with a big name and a big number. Depth-of-field blur and warm light streaks on a cool dark scene. | `poster-spec.html`: "spec out" a cold email, a reply, a booked meeting, a list record, a domain setup |
| 3 | `03-object-pun-keycap.jpg` | Huge, tight, black uppercase type on off-white, finished by one realistic orange object that *is* the last word of the sentence. | `poster-object-pun.html`: one-liners and wit (keycaps, toggles, stamps, tags) |
| 4 | `04-big-type-3d-props-pills.jpg` | A stacked verb list in giant type ("Shoot. Edit. Deliver. Repeat.") with small tilted pill labels overlapping the words and a few 3D props floating around, on a light grid. | Build from parts: stacked words in Poppins, `.kpill`/`.gpill` tags tilted ±3–6°, props as SVG or the mascot. Works on `cm paper` or black. |
| 5 | `05-object-hero-calculator.jpg` | Setup line on top ("For years, the formula was…"), then a big realistic object cropped off the bottom edge with the punchline on its screen. One accent word in colour. | `poster-object-pun.html` variant: object cropped at the bottom, text on its display (calculator, phone, terminal, receipt) |
| 6 | `06-floating-glass-pills-phone.jpg` | A realistic phone or app screen in the centre with frosted glass pills (icon + label) floating around it at angles, one larger glass card with a bold statement, cinematic light behind. | Combine `poster-ui.html` (device) + `.glass` pills from `poster-glass-steps.html`. Put Cymate outcomes on the screen and services on the pills. |
| 7 | `07-sketch-over-photo.jpg` | Simple hand-drawn line illustrations over a real photo, as if drawn on the scene: little stick figures working, a handwritten headline, a hanging sign. | Darkened office/desk photo or stock (`--bg`) + inline SVG line art in white or orange + `Permanent Marker`/handwritten headline. Never redraw the mascot; draw generic figures. |

| 8 | `08-official-linkedin-banner-champions.jpg` | **Cymate’s own LinkedIn banner (official “Champions” look).** Brushed dark-metal background with diagonal speed streaks, orange motion streaks bottom-left, the tagline “OUTBOUND FOR CHAMPIONS” in condensed Bebas Neue fading white to orange, the orange monogram tile right after it, and a huge ghosted mascot (black fill, thin grey line art) cropped off the right edge. | `champions/gen_champions_banner.py` (YouTube banner B07); five more Champions layouts (stacked, orange, spotlight, speed burst, minimal) in `champions/gen_champions_variants.py`. Use the look (streaks, condensed type, ghost mascot) where it fits, with or without the tagline; keep Poppins/Inter for post body copy. Ghost mascot asset: `assets/brand/mascot-ghost-dark.png`. |

## What makes them work (apply to every Cymate post)
- **One hero, lots of air.** The object or card stack owns 40–60% of the canvas; everything else is small and quiet.
- **Weight contrast in type.** Light/regular for the setup, heavy or orange for the payoff word.
- **Real-looking materials.** Glass with blur and a bright top edge, plastic with an inner bevel and soft contact shadow, paper with slight warmth. Soft light falloff instead of flat fills.
- **Small technical details** (numbers like 01–04, tracked micro labels, hairline rules, orbit lines) signal polish and expertise. Keep them tiny.
- **Warm light, not decoration.** Orange glow sits behind the hero like a light source; it never becomes a flat orange block (unless the post uses the burnt-orange background).

## Guardrails
- Don't copy any reference's layout, words, product or brand. If someone could put the two side by side and call it a copy, change it.
- Stay inside the brand standard: professional, sharp, clean, a little fun. Orange `#FF5A00` family only for accents (no purple, no blue of any kind, no cobalt blue from refs 5 and 6).
- Off-white (`cm paper`) is allowed for refs 3, 4 and 5 style posts, about one post in five. Use the dark wordmark automatically (the header swaps it).
