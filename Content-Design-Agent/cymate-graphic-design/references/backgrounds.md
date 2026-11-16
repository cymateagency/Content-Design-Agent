# Stock backgrounds (stills and footage)

A background image or clip can add mood behind a post or Reel, as long as it never competes with the content.

## The rule
- Opacity **20–30%** (default 25%). Set with `--bg-opacity 0.20–0.30`; the scripts clamp anything outside that.
- Greyed and slightly darkened, with an edge fade, over the black base. The ember glow and all content sit on top.
- It supports the topic (an office, a laptop, a city at night, hands typing, a desk, abstract motion) and has no readable text, logos or recognisable faces of strangers.
- If, at a glance, the eye goes to the background before the headline, lower it or drop it.
- Counts as the design's one texture: don't add dots or grid on top of a photo unless it's very faint.
- Use it in about one post in three, not every time.

## Where to get them
Use sources that license images and video for commercial use without attribution: **Pexels, Unsplash, Pixabay, Mixkit (video), Coverr (video)**. Download the largest HD size (stills ≥ 1920 px on the long side, video ≥ 1080p).

**Pinterest**: fine for finding an idea or a look, but pins are usually someone else's copyrighted photo with no licence. Only use a Pinterest find if it traces back to a free-licence source like the ones above, or to the team's own photos. Never pull Cymate or client logos, celebrity photos or film stills from Pinterest.

## Getting the file into the render
The sandbox can't download from stock sites directly, so:
1. Search (web search or image search) and give Ken 2–3 specific picks with links, each with one line on why it fits.
2. Ken downloads the chosen file and uploads it to the chat (or the project).
3. Render with `--bg <file>` for stills or `--bg-video <file>` for Reels.
If an org owner adds the stock sites (e.g. images.pexels.com, images.unsplash.com, cdn.pixabay.com) to the sandbox's allowed domains, download directly instead.

## In templates
Stills: add `<div class="tx tx-stock" style="background-image:url('{{BG}}')"></div>` as the first layer inside `.cm`, before `{{HEADER}}`. Add class `full` to skip the edge fade.
Reels: pass `--bg` or `--bg-video` to `make_reel.py`; no template change needed.
