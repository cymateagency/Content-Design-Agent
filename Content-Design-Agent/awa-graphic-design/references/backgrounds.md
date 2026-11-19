# Backgrounds

## The soft red glow (default, the "deep maroon" look)
AWA has no maroon colour. The deep maroon look is AWA Red `#CF0101` light fading into black `#000000`, so the transition between them reads as maroon. Build it with radial gradients of `rgba(207,1,1,a)` over `#000000`, never with a separate dark-red hex.

- **`.aw` (default)**: black with red light rising from below (a wide ellipse centred under the bottom edge, ~60% red at the source fading to 0) plus a faint red lift in one top corner.
- **`.aw.glow-corner`**: the light comes from the bottom-right corner. Good for photo and device layouts.
- **`.aw.glow-top`**: the light comes from above. Good for BOF "spotlight" posts (ticket, badge).
- **`.aw.black`**: pure black, for full-bleed photos that bring their own light.
- Add depth with blur: soft blurred red shapes (`.blur-glow`) behind the hero, halos behind people, a backlit crowd blurred by distance (CP-002).
- One light source per post. The glow sits behind the hero like a light, it never becomes a flat red block (unless the post uses the solid red background).

## Solid red
`.aw.red`: AWA Red with a soft white lift top-left and a faint black falloff bottom-right. White text, black accents, the all-white logo (the header swaps it automatically). Good for CTA slides, report-card headers, ticket bodies.

## White
`.aw.white`: white with a very faint red glow in one corner. Black text, red accent, the dark logo (automatic). Use it to alternate the feed: if the previous post was dark-dominant, make the next cover white-dominant, and vice versa (taste.md, from CP-012).

## Paper (scrapbook and letter posts only)
`.aw.paper`: Paper `#F6F1EA`. Black text, red accent, the dark logo (automatic). Only for scrapbook and letter-style posts (torn notes, polaroids, letters, report-style paper props inside those posts). Never as a general light background: use white for that.

## Texture (at most one per design)
- `tx-hexes` (a faint dot grid that echoes the hexagon) or `tx-diamonds` (the diamond line pattern), both masked to fade out.
- Film grain is built into the header and added by `finish.py`.
- A darkened photo (`tx-photo`) or a stock background (below) counts as the texture.

## Stock backgrounds (stills and footage)
- Opacity **20–30%** (default 25%), set with `--bg-opacity 0.20–0.30`; the scripts clamp anything outside that.
- Greyed and slightly darkened, with an edge fade, over the black base. The red glow and all content sit on top.
- It supports the topic (an agency office, a team table, a studio, laptops, a city at night) and has no readable text, logos or recognisable faces of strangers.
- If, at a glance, the eye goes to the background before the headline, lower it or drop it.
- Sources that license images and video for commercial use without attribution: Pexels, Unsplash, Pixabay, Mixkit (video), Coverr (video). Download the largest HD size. Pinterest is for ideas only unless a find traces back to a free-licence source.
- Getting the file in: suggest 2–3 specific picks with links and one line each on why they fit; the user downloads the chosen file and supplies it; render with `--bg <file>` (stills) or `--bg-video <file>` (Reels).
- In templates: `<div class="tx tx-stock" style="background-image:url('{{BG}}')"></div>` as the first layer inside `.aw`. Add class `full` to skip the edge fade.
- QA's off-palette check may flag a colourful photo: grade it down (the `.tx-stock` filter already desaturates) so no non-red hue shows.
