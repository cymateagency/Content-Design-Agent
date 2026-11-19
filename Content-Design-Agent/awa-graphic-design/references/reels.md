# Reels (teach, then pivot)

A Reel (1080 × 1920, 9:16) teaches one useful thing about agency culture, then turns into what AWA stands for. The lesson has to stand on its own. Never open with the brand.

## Structure (default 15 s)
| Beat | Time | What happens |
|---|---|---|
| Hook | 0–2.5 s | One line that names an agency moment. Movement in the first 0.3 s. Readable without sound. |
| Teach | 2.5–9 s | 2–3 quick beats, one idea each, ~6–10 words on screen. |
| Transition | ~0.8 s | Default: the red panel wipe carrying a white hexagon (built into `reel-transition.html`). |
| Pivot | 3 s | The better way, in 2–3 short chips tied to the lesson. TOF stays soft; BOF can point to nominations. |
| End card | 2–3 s | Logo, one CTA that matches the stage and caption. |

Other transitions to rotate: zoom punch on the last word, card flip, "but wait" freeze, before/after split. Build them in CSS keyframes on the same timeline.

## Sound
`make_reel.py` calls `make_audio.py`, which synthesises an original music bed and sound effects from scratch (no samples), mixed to about −14 LUFS. Styles: `chill` (template default, warm and human), `drive`, `hype`, `tension`; `drop` = the second of the transition's impact. SFX cues (`thud`, `pop`, `tick`, `click`, `riser`, `whoosh`, `impact`, `glitch`, `ding`), one per visible motion. Two files: `<name>.mp4` (music + SFX) and `<name>-sfx.mp4` (SFX only, to pair with a trending sound added in-app). Never bake in music AWA doesn't own; `--music track.mp3` for a licensed track.

## Safe zones
Text between y = 260 and y = 1540, clear of the right 150 px below y = 1100. Hook text inside the centre 1080 × 1350 so the grid cover reads. Every beat on screen at least 1.8 s.

## Render and check
```bash
python3 scripts/make_reel.py reel.html out/reel-name.mp4 --preview
python3 scripts/make_reel.py reel.html out/reel-name.mp4 --bg-video stock.mp4 --bg-opacity 0.25 --preview
```
View the contact sheet and frames at the hook, a teaching beat, the transition and the end card. Check the sound with a spectrogram (`ffmpeg -i out.mp4 -filter_complex "showspectrumpic=s=1400x300:legend=1:scale=log" spec.png`).

## Delivery
Both MP4s + cover PNG, caption, the music style used, an optional trending sound to pair with the SFX-only file, alt text.
