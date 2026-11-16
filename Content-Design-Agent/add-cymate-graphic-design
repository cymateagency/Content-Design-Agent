# Cymate brand and design

Cymate (cymate.io) is a US-based B2B cold outbound agency. Social content focuses on GTM (cold email, deliverability, list building, reply rates, booked meetings) and exists to win customers. The look is **premium and high-production, but never stiff**: posts range from fun and meme-driven to sleek and editorial, and every one should make someone stop scrolling.

The posted series (samples: 50+ Reply Velocity, Why Us, Ways to Say I Love You, What We Do, Fast Pivots, Replies Per Day, POV scale, Vitamin C, Cold Email Insight, List Quality, Put a Finger Down, Don’t Swipe, Brand New Day) is the reference for the vibe. Match that energy, then push it further with fresher ideas and better execution.

## Tagline
**“Outbound for Champions”** is Cymate’s official tagline (LinkedIn banner). It is optional, not a requirement: don’t add it to every asset or use it as a default kicker. Reach for it only when it clearly helps (channel art, a brand moment). When used, write it exactly like that, in caps when set in Bebas Neue. Everything else gets its own headline and concept.

## Brand standard
Professional, sharp, clean, and a little fun, so enterprise buyers trust Cymate on sight: polished visuals, clear writing, and proof we know our stuff. In practice: premium finish over gimmicks, restraint over noise, specific expertise over hype, and playfulness as seasoning, never the whole dish. Trend and meme posts still have to look like a serious company made them.

## Background
- **Default: near-black (`#070707`) with a soft charcoal lift in one corner and a faint warm orange ember in the other.** No blue anywhere: no blue haze, no blue gradients, no blue glows, no blue dots, no blue UI accents. (The blue haze was retired in November 2026.)
- Add depth with **one texture**, not colour: neutral dot halftone (`tx-dots`), fine grid (`tx-grid`), film grain (built into the header), topographic or wave line art drawn in SVG, or a darkened photo (`tx-photo`, user-supplied via `--bg`).
- **Burnt orange** (`cm orange`) is an occasional variety option, at most about one post in four.
- **Off-white paper** (`cm paper`) for object-pun and big-type posts (see `inspiration.md` #3–5), about one post in five; the header switches to the dark wordmark on its own. Plain grey `cm light` only when asked.

## Colours
| Role | Value |
|---|---|
| Base black | `#050609` |
| Charcoal lift | `rgba(255,255,255,.045)`, one corner |
| Ember glow | `rgba(255,90,0,.07–.08)`, one corner |
| Brand orange | `#FF5A00` (≈ `#FD5E02`) |
| Signature gradient | `#C21A00 → #FF5A00 → #FFC09A` (deep red to orange to peach), on numbers, key words, pill borders, CTA pills |
| Chrome | white to `#9A9EA8` vertical gradient, for big uppercase statements |
| White / muted white | `#FFFFFF` / `rgba(255,255,255,.72)` |
| Glass | white at 3–10% with a 16% border |

- **Cyan `#00E6FF` is retired**, even though older posts (POV, Cold Email Insight, List Quality) use it.
- Trend props may carry their own colours inside the prop only (red and green flags, a calendar icon’s red).

## Logo (official, from the logo-variation file, updated Nov 2026)
The logo is the **ninja-cat mascot** plus the custom chunky **CYMATE.** wordmark with an orange square dot (`#FD5E02`). The hex icon and the old geometric wordmark are retired; never use them or retype the wordmark in a font.

Official set in `assets/brand/` (transparent PNG + SVG, use the SVG when something needs to scale):
| File | Use |
|---|---|
| `wordmark-white` / `wordmark-dark` | header, footers, small sign-offs |
| `logo-stacked-white` / `logo-stacked-dark` | mascot over wordmark: end cards, CTA slides, Reel outros, covers |
| `mascot-white` / `mascot-dark` | mascot alone with its white keyline: icons, avatars, heroes, transitions |
| `monogram-outline-white` / `monogram-outline-dark` | stacked CY/MA/TE in a rounded outline box: stickers, corner marks, favicons |
| `monogram-orange-on-dark` (black letters) / `monogram-orange-on-light` (white letters) | filled orange tile: profile pictures, app-icon style marks, watermarks |

Render tokens: `{{LOGO}}` white wordmark, `{{LOGO_DARK}}` dark wordmark, `{{ICON}}` small mascot, `{{MASCOT}}` large mascot, `{{LOCKUP}}` / `{{LOCKUP_DARK}}` stacked logo, `{{MONOGRAM}}` orange tile. For anything else, embed the file from `assets/brand/` as a data URI or pass it with an override flag.

- Header on every poster (`{{HEADER}}`): white wordmark top-left, mascot top-right.
- Use white versions on black, orange and photo backgrounds; dark versions only on light backgrounds.
- There is no official horizontal lockup (mascot beside the wordmark). Don't assemble one; use the stacked logo, or the wordmark and mascot as separate elements (like the header).
- Don't recolour, stretch, crop, outline, rotate or add effects (the soft drop shadow on the header mascot is the only exception). Keep clear space around each mark of at least the height of the orange dot.
- The mascot can be a character in posts (peeking from an edge, reacting, holding a prop), always as the supplied artwork; never redraw or restyle it.

## Social bar
Every single-image poster ends with the social pill (`{{SOCIAL_BAR}}`): YouTube @CymateLLC, Instagram @cymate.io, LinkedIn Cymate, website cymate.io. Carousels show it on the last slide only.

## Type
- **Poppins** is the house face: ExtraBold/Black for headlines (sentence case or uppercase), Light/Regular for subheads.
- **Inter** for body copy and realistic UI text.
- **Display faces by mood**, one per design: Bungee (blocky, techy), Luckiest Guy (fun, meme), Rubik Dirt (distressed, gritty), Anton (tall, news), Archivo Black (bold), Unbounded (chunky, wrapped-style), Space Grotesk (techy), Instrument Serif italic (premium contrast), Permanent Marker (handwritten note), IBM Plex Mono (labels, data).
- Poppins has no arrow glyph: draw arrows as inline SVG.

## Signature elements
- Gradient-outline kicker pill (`.kpill`) and gradient-filled pill (`.gpill`).
- Gradient text (`.grad-text`) on the number or the 1–3 key words; chrome text (`.chrome-text`) for big uppercase lines.
- Frosted glass cards (`.glass`) and gradient-framed boxes (`.gframe`).
- Realistic props and UI: notifications, search bars, inboxes, receipts, calendars, charts.
- Darkened team or office photos, or stock backgrounds at 20–30% opacity, under the content (see `backgrounds.md`).

## Wesley
Wesley can front a poster for recognition, not every time. Use only photos the user supplies (a cutout PNG with a transparent background works best), passed with `--photo` or bundled as `assets/wesley.png`. Never generate or alter his likeness, and never pull photos from the web.

## Direction
- **Aim for**: a scroll-stopping hero element, strong contrast, a curiosity gap in the headline, readable at phone size in under two seconds, and real production polish (soft shadows, believable materials, consistent light).
- **Avoid**: any blue (backgrounds, gradients, glows, dots, UI accents), more than one texture, clutter, generic stock-icon looks, guru clichés (yellow arrows, money emoji), cyan, and copying the samples outright.
