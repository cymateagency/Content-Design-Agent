# AWA brand and design

Agency Workplaces (AWA) is a workplace culture recognition platform for agencies. Social content talks to agency owners, founders and leaders about recognition, retention, trust, growth and being seen, and moves them through the funnel (`funnel.md`). The look is **soft, warm and premium, never flat**: black with red light rising from below, rounded Poppins headlines, real people and real objects, and depth from blur, overlap and soft shadows.

## Tagline
AWA has no tagline. Don't invent one, and don't reuse a past headline as a tagline.

## Colours
AWA uses three colours, plus two limited extras. Nothing else, ever: no new colours, no tints sold as "brand" colours, no second accent.

| Role | Value | Use |
|---|---|---|
| AWA Red (accent) | `#CF0101` | highlights, accent words, pills, panels, glows, the solid red background |
| Black (base) | `#000000` | default background, text on white |
| White (base) | `#FFFFFF` | text on black and red, the white background, cards |
| Bright red (limited) | `#FF3B3B` | **only** for red text on black or dark backgrounds, so it stays readable (`--accent-text` does this automatically) |
| Paper (limited) | `#F6F1EA` | **only** for scrapbook and letter posts (torn notes, polaroids, letters), via `.aw.paper` |

- **There is no separate maroon or deep red colour** (the old `#9A0000` is gone). The deep maroon look is a *background treatment*: AWA Red light fading into black. See `backgrounds.md`.
- No sticky-note yellow (the old `#FFF6A8` is gone): notes are white or paper.
- Transparency of the three colours is fine (a 60% white subline, a red glow at 40%), as is a blur of them. A new hue is not.
- Red text on black uses Bright red `#FF3B3B`, never `#CF0101` (too dark to read on black). On white and paper, red text is `#CF0101`; on red, accent text is white.
- UI props (a phone, a lock screen) stay in black, white and greys of them. No real app colours.
- `#CF0101` is the AWA red. TODO: the current logo files still use `#CC0000` for the red mark; they need updating to `#CF0101`. Never recolour the logo yourself; swap in the updated files when they arrive.

## Logo (official AWA logo: hexagon mark + "AGENCY WORKPLACES")
Files in `assets/brand/` (PNG + SVG; the SVGs wrap the same artwork):

| File | Use | Render token |
|---|---|---|
| `awa-logo-light` | red mark, white words: black, dark and photo backgrounds | `{{LOGO}}` |
| `awa-logo-dark` | red mark, black words: white backgrounds | `{{LOGO_DARK}}` |
| `awa-logo-white` | all white: red backgrounds, where the red mark would disappear | `{{LOGO_WHITE}}` |

- The header (`{{HEADER}}`) puts the logo top-left at 48 px tall and swaps the version by background class (`.aw` light, `.aw.white` dark, `.aw.red` white). Keep the logo small with its own breathing room above the copy.
- Never retype "Agency Workplaces" or "AWA" as a fake logo (QA flags it), recolour, stretch, crop, outline, rotate or add effects to the logo.
- Size and clear space: on posts the logo is about 48 px tall (never smaller than that on a 1080-wide canvas), with at least the hexagon mark's height clear on every side.
- TODO: add the Workplace Award badge (e.g. `assets/brand/awa-badge-<year>.png`) for BOF posts. Until it exists, don't draw a fake badge as if it were the real one.

## No social bar
AWA posts carry the logo only: no handles bar. The website is agencyworkplaces.com (used on CTA slides).

## Type
Three fonts, nothing else.
- **Poppins**: everything by default. Headlines mix light (300) and bold (700/800) in one line, tight tracking (−0.04 to −0.05 em), tight leading (0.95–1.05). Body and sublines light or regular, 1.25–1.45 leading. The default soft look uses rounded Poppins headlines (taste.md).
- **Anton** (`.display`): big condensed statement headlines, all caps (the "GOOD PEOPLE STAY WHERE THEY'RE SEEN" look), report-card grades, ticket titles. One Anton block per post at most.
- **Caveat** (`.hand`): short handwritten notes, stickers, margin comments, polaroid captions. Short phrases only, never inside a headline.
- Accent word in a headline: Poppins light italic in red (`.it-red`), or bold in an otherwise light line.
- Poppins has no reliable arrow glyph: draw arrows as inline SVG.

## Signature devices (use when they fit, one or two per post, never all at once)
- White pennant ribbon highlighting one word (`.pennant`)
- The hexagon from the logo, as a shape, outline or medal (`.hex`)
- Diamond line pattern (`.diamonds`, `.tx-diamonds`)
- Red name bar under a person's photo (`.namebar`)
- Quote frame with an open corner (`.qframe`), for real quotes only
- Frosted glass panels (`.glass`) over photos and glows
- Real-world props: lock screens, phones mid-scroll, tickets, report cards, polaroids, torn paper

## People and photos
Real photos of people beat illustrations: a cut-out team photo overlapping a panel edge beats a faceless figure. Use only photos the user supplies (`--photo`, ideally a transparent cut-out PNG, or `--bg`). Never generate or alter anyone's likeness, never pull photos of people from the web. Keep cut-outs clear of text and pills. Real names, titles and quotes only when the user provides them.

## Direction
- **Aim for**: one real-world hero, soft red light, a hook that names an agency moment, readable on a phone in under two seconds, depth (overlap, blur, shadows, cropping off the edge).
- **Avoid**: type on flat colour alone, more than 3 text levels on a static, emoji in designs, any colour outside red/black/white, clutter, generic stock-icon looks, copying references outright.
