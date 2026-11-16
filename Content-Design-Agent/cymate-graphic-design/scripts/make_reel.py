#!/usr/bin/env python3
"""Render an animated Cymate Reel (HTML + CSS keyframes) to a 1080x1920 MP4, plus a cover PNG.

Usage:
  python3 scripts/make_reel.py reel.html out/reel-name.mp4 [--fps 30] [--duration 15]
        [--bg-video stock.mp4 | --bg stock.jpg] [--bg-opacity 0.25] [--music licensed.mp3] [--no-music] [--no-sfx]
        [--silent] [--preview]

How it works
- The template is built exactly like a poster (fonts, header, logo, mascot, lockup) by render.py.
- Every CSS animation lives on one global timeline (animation-delay = when it starts, in seconds).
  The script pauses all animations and seeks them frame by frame, so timing is exact and repeatable.
- Duration comes from <meta name="reel-duration" content="15"> (or --duration). The cover frame time
  comes from <meta name="reel-cover" content="1.2"> (default 1.0s) and is saved as <name>-cover.png.
- --bg-video / --bg: stock footage or a still, laid under the design at --bg-opacity (0.20-0.30),
  greyed and darkened so it adds mood without pulling focus. The design's own black base is made
  transparent and composited over it with ffmpeg; the blue haze stays on top.
- Sound (make_audio.py): an original synthesized music bed (style/bpm/drop from <meta name="reel-music">) plus
  sound effects timed from <meta name="reel-sfx">, all generated from scratch and royalty-free.
  Writes two files: <name>.mp4 (music + SFX) and <name>-sfx.mp4 (SFX only, for pairing with a trending sound
  added in the Instagram/TikTok app). --music swaps in a licensed track the team owns instead of the bed.
  --no-music / --no-sfx drop one layer; --silent exports no audio at all.
- --preview: also writes a 6-frame contact sheet (<name>-sheet.png) for the visual check.
"""
import argparse, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render  # noqa: E402

SEEK_JS = "async (t) => { for (const an of document.getAnimations()) { an.pause(); an.currentTime = t * 1000; } await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }"  # double rAF: make sure the compositor has painted the seeked frame before the screenshot


def meta(html, name, default):
    m = re.search(rf'<meta\s+name="{name}"\s+content="([\d.]+)"', html)
    return float(m.group(1)) if m else default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    render.add_common_args(ap)
    ap.set_defaults(width=1080, height=1920)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--duration", type=float)
    ap.add_argument("--bg-video", help="stock video clip (mp4/mov/webm) the user supplied")
    ap.add_argument("--music", help="licensed track to use instead of the generated music bed")
    ap.add_argument("--no-music", action="store_true")
    ap.add_argument("--no-sfx", action="store_true")
    ap.add_argument("--silent", action="store_true", help="export without any audio")
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()

    src_text = pathlib.Path(a.html).read_text()
    dur = a.duration or meta(src_text, "reel-duration", 15.0)
    cover_t = meta(src_text, "reel-cover", 1.0)
    layered = bool(a.bg_video or a.bg)
    # When a stock layer is used, drop the base black so ffmpeg can put the footage underneath.
    extra = ".cm{background-color:transparent!important} html,body{background:transparent!important}" if layered else ""
    still_bg, a.bg = a.bg, None  # the still goes through ffmpeg too, not the template
    tmp = render.build_html(a.html, a, extra_css=extra)

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    frames = pathlib.Path(f"/tmp/_reel_frames_{out.stem}")
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir(parents=True)
    n = int(round(dur * a.fps))

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--disable-threaded-animation", "--disable-gpu-compositing"])  # seeked frames must match what is painted
        pg = b.new_page(viewport={"width": a.width, "height": a.height})
        pg.goto(f"file://{tmp}")
        pg.wait_for_timeout(600)
        clip = {"x": 0, "y": 0, "width": a.width, "height": a.height}
        warned = set()
        for i in range(n):
            t = i / a.fps
            pg.evaluate(SEEK_JS, t)
            if i % a.fps == 0:  # overflow check once per second
                for w in pg.evaluate(render.CHECK_JS):
                    if w not in warned:
                        warned.add(w)
                        print(f"WARN t={t:.1f}s", w)
            pg.screenshot(path=str(frames / f"{i:05d}.png"), clip=clip, omit_background=layered)
        b.close()
    print(f"rendered {n} frames")

    ff = ["ffmpeg", "-y", "-loglevel", "error"]
    # film finish to match finish.py: lighter on paper/light backgrounds (a dark vignette looks dirty there)
    light_bg = bool(re.search(r'class="cm[^"]*\b(paper|light)\b', src_text))
    fin = "noise=alls=3:allf=t" if light_bg else "noise=alls=4:allf=t,vignette=PI/5"
    op = min(max(a.bg_opacity, 0.20), 0.30)
    grade = f"scale={a.width}:{a.height}:force_original_aspect_ratio=increase,crop={a.width}:{a.height},hue=s=0.5,eq=brightness=-0.06:contrast=1.05,vignette=PI/4,format=rgba,colorchannelmixer=aa={op}"
    if a.bg_video:
        inputs = ["-stream_loop", "-1", "-i", a.bg_video]
    elif still_bg:
        inputs = ["-loop", "1", "-i", still_bg]
    else:
        inputs = []
    cmd = ff + ["-framerate", str(a.fps), "-i", str(frames / "%05d.png")] + inputs
    if inputs:
        fc = (f"color=c=0x070707:s={a.width}x{a.height}:r={a.fps}:d={dur}[base];"
              f"[1:v]{grade}[bg];[base][bg]overlay=shortest=1[under];[under][0:v]overlay=shortest=1,{fin},setsar=1,format=yuv420p[v]")
        cmd += ["-filter_complex", fc, "-map", "[v]"]
    else:
        cmd += ["-vf", f"{fin},setsar=1,format=yuv420p", "-map", "0:v"]
    silent_vid = out.with_name(out.stem + "-silent.mp4") if not a.silent else out
    cmd += ["-t", str(dur), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(a.fps), "-movflags", "+faststart", str(silent_vid)]
    subprocess.run(cmd, check=True)

    if not a.silent:
        import make_audio
        from scipy.io import wavfile
        mixes = [(out, a.no_music, a.no_sfx)]
        if not a.no_music and not a.no_sfx:
            mixes.append((out.with_name(out.stem + "-sfx.mp4"), True, False))
        for target, nm, ns in mixes:
            buf, style, bpm = make_audio.build(src_text, dur, nm, ns, a.music)
            wav = pathlib.Path(f"/tmp/_reel_audio_{target.stem}.wav")
            wavfile.write(wav, make_audio.SR, (buf * 32767).astype("int16"))
            base = ff + ["-i", str(silent_vid), "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:v", "copy"]
            tail = ["-c:a", "aac", "-b:a", "192k", "-t", str(dur), "-movflags", "+faststart", str(target)]
            try:
                subprocess.run(base + ["-af", "loudnorm=I=-14:TP=-1.5:LRA=11"] + tail, check=True)
            except subprocess.CalledProcessError:  # very short clips can't be loudness-normalised
                subprocess.run(base + tail, check=True)
            print("saved", target, "" if nm else f"(music: {'licensed track' if a.music else f'{style} {bpm:g} bpm'})")
        silent_vid.unlink()
    else:
        print("saved", out)

    cover = out.with_name(out.stem + "-cover.png")
    subprocess.run(ff + ["-ss", str(cover_t), "-i", str(out), "-frames:v", "1", str(cover)], check=True)
    print("saved", cover)
    if a.preview:
        sheet = out.with_name(out.stem + "-sheet.png")
        step = max(dur / 6, 0.5)
        subprocess.run(ff + ["-i", str(out), "-vf", f"fps=1/{step},scale=360:-1,tile=6x1:padding=8:color=0x222222", "-frames:v", "1", str(sheet)], check=True)
        print("saved", sheet)
    shutil.rmtree(frames, ignore_errors=True)


if __name__ == "__main__":
    main()
