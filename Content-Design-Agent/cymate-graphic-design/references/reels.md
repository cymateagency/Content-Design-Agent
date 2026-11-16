# Reels (trend transition: educate, then pivot to Cymate)

Reels are short vertical videos (1080 × 1920, 9:16) that teach one useful thing, then turn with a trending-style transition into what Cymate does and how it helps. The education has to stand on its own: if the viewer stopped before the pivot, they should still have learned something. That is what earns the pivot.

## Structure (default 15 s, range 10–30 s)
| Beat | Time (15 s) | What happens |
|---|---|---|
| Hook | 0–2.5 s | One line that names a pain or opens a gap. Movement in the first 0.3 s (slam, pop, zoom). Readable without sound. |
| Teach | 2.5–9 s | 2–3 quick beats, one idea each, ~6–10 words on screen per beat. Real, specific, useful. |
| Transition | ~0.8 s | The trend move (see below). This is the moment the video changes from "lesson" to "Cymate". |
| Pivot | 3 s | "Or let us handle it": what Cymate does, in 2–3 short chips tied to the lesson just taught. |
| End card | 2–3 s | Logo lockup, one CTA matching the caption, social bar. |

Keep about 60–70% of runtime educational. Never open with the brand.

## Transition library (pick one per Reel, rotate them)
- **Mascot wipe** (default, built into `reel-transition.html`): the orange gradient panel sweeps across with the ninja-cat mascot riding it, white flash, pivot appears. Brand-ownable; use it most often.
- **Zoom punch**: the last teaching word scales up until it fills the frame, cut to black, pivot slams in.
- **Glitch cut**: 3–4 frames of RGB-split jitter on the last beat, then hard cut.
- **Swipe / whip pan**: whole scene slides out sideways with motion blur, the pivot slides in from the other side.
- **Card flip**: the teaching card flips in 3D to reveal the Cymate answer on its back.
- **"But wait" freeze**: freeze the last beat, desaturate, a kpill "But…" pops, then pivot.
- **Before / after split**: screen splits; left "doing it yourself", right "with Cymate".
Build these in CSS keyframes on the same global timeline. Each new transition that works well can become its own template.

## Trend formats that map well to this structure
POV · "3 signs your…" · "Stop doing this" · "Things I wish I knew before…" · "Nobody talks about…" · "Rate my cold email" · expectation vs reality · "Wait for it" · countdown · "Tell me you… without telling me". Check `trends.md` for what is current.

## Sound (music bed + sound effects, built in)
Every Reel ships with sound. `make_reel.py` calls `make_audio.py`, which synthesizes an **original** music bed and sound effects from scratch: no samples, no borrowed songs, so Cymate owns it and it can't be muted or claimed. It's mixed and normalised to about −14 LUFS (social loudness).

**Music bed** (`<meta name="reel-music" content="style=drive; bpm=118; drop=9.62; key=A">`)
- `drive`: punchy house-pop, four-on-the-floor. Default; fits most educational-to-pivot Reels.
- `chill`: lo-fi swing and warm keys. Calm explainers, story-style posts.
- `hype`: trap-style half-time with an 808. Bold claims, results, countdowns.
- `tension`: dark pulse that explodes at the drop. "Stop doing this" and myth-busting hooks.
- `drop` = the second of the transition's impact. Before it the bed is filtered and sparse (teaching); at the drop it opens up (selling). Rotate styles across Reels and log which one was used.

**Sound effects** (`<meta name="reel-sfx" content="seconds:effect, ...">`), one cue per visible motion:
| Effect | Use on |
|---|---|
| `thud` | headline line slams in |
| `pop` | pill, chip or kicker pops |
| `tick` / `click` | kicker labels, counters, UI taps |
| `riser` | the ~0.9 s before a transition |
| `whoosh` | wipes, swipes, whip pans (pans left to right) |
| `impact` | the drop / flash, same time as `drop` |
| `glitch` | glitch-cut transitions |
| `ding` | logo or end card appears |
Don't stack more than ~2 effects per second, and leave a gap after the impact so the music carries the pivot. When you move an animation, move its cue to the same second.

**Files delivered**: `<name>.mp4` (music + SFX) and `<name>-sfx.mp4` (SFX only). Use the second one when posting with a trending sound added in the Instagram/TikTok app: that's how trending audio gets credited, and the SFX still land on the motion. `--music track.mp3` swaps in a licensed track the team owns instead of the generated bed. Never bake in a commercial or trending song pulled from elsewhere. `--no-music`, `--no-sfx` and `--silent` drop layers.

**Check**: you can't listen, so render a spectrogram (`ffmpeg -i out.mp4 -filter_complex "showspectrumpic=s=1400x300:legend=1:scale=log" spec.png`) and confirm the hits line up with the cue times and the drop, and that ebur128 reports about −14 LUFS with the peak under −1 dB.

## On-screen text and safe zones
- Text between y = 260 and y = 1540; clear of the right 150 px below y = 1100 (like/comment buttons).
- Hook text inside the centre 1080 × 1350 so the grid cover still reads.
- Every beat on screen at least 1.8 s; ~3 words per second max reading speed.
- Burned-in text does the work; viewers watch muted.

## Build and render
1. Copy `templates/reel-transition.html`, replace the copy, adjust scene times in the `--in/--out/--d` values. Duration lives in `<meta name="reel-duration">`, the cover frame in `<meta name="reel-cover">`.
2. Render:
```bash
python3 scripts/make_reel.py reel.html out/reel-name.mp4 --preview
python3 scripts/make_reel.py reel.html out/reel-name.mp4 --bg-video /mnt/user-data/uploads/stock.mp4 --bg-opacity 0.25 --preview
python3 scripts/make_reel.py reel.html out/reel-name.mp4 --bg /mnt/user-data/uploads/stock.jpg --preview
```
Outputs the MP4, `<name>-cover.png` (Reel cover) and with `--preview` a contact sheet. A 15 s Reel takes roughly a minute.
3. Visual check: view the contact sheet and pull frames at the hook, mid-teach, the transition and the end card (`ffmpeg -ss <t> -i out.mp4 -frames:v 1 f.png`). Check timing, legibility, safe zones and that no WARN lines were printed.

## Delivery for a Reel
Both MP4s (full mix and SFX-only) + cover PNG, caption (voice rules apply), the music style used, an optional trending sound to pair with the SFX-only version, alt text, and the trend used and why.
