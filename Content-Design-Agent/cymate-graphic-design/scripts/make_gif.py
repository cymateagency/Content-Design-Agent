#!/usr/bin/env python3
"""Render an animated Cymate template to a seamless, LinkedIn-ready looping GIF (plus an MP4 twin).

Usage:
  python3 scripts/make_gif.py anim.html out/name.gif [--fps 15] [--loop 3] [--width 1080 --height 1350]
        [--out-width 1080] [--max-mb 5] [--mp4]

How the loop stays seamless
- Every animation in the template must repeat with a period that divides the loop length
  (<meta name="gif-loop" content="3">): envelopes moving one slot along a track, belts sliding one dash,
  lights blinking twice per loop. Frame 0 and frame N are then identical, so the GIF never jumps.
- Frames are taken at t = i / fps for i in [0, loop * fps), seeking every animation (same method as make_reel).

File size
- LinkedIn accepts animated GIFs up to 5 MB per image (250 frames max). The script builds one optimised palette
  for the whole loop and only re-encodes changed rectangles. If the file is still over --max-mb it steps down the
  output width (1080 → 960 → 864 → 720), then the frame rate, until it fits, and says what it did.
- Big moving flat areas (marquees, kinetic type): use --dither none --colors 48, which can cut the file 5-10x.
- Flat colours compress best: no film grain, no big soft gradients, no photos for GIFs. finish.py is NOT applied.
--mp4 also writes an MP4 of the same loop (repeated to ~9 s) for platforms that prefer video.
"""
import argparse, os, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render  # noqa: E402

SEEK_JS = "async (t) => { for (const an of document.getAnimations()) { an.pause(); an.currentTime = t * 1000; } await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }"  # double rAF: make sure the compositor has painted the seeked frame before the screenshot


def encode(frames, fps, out, width, colors=192, dither='bayer'):
    pal = frames / "palette.png"
    dmode = 'bayer:bayer_scale=4' if dither == 'bayer' else dither
    scale = f"scale={width}:-1:flags=lanczos"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(frames / "%04d.png"),
                    "-vf", f"{scale},palettegen=max_colors={colors}:stats_mode=full", str(pal)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(frames / "%04d.png"), "-i", str(pal),
                    "-lavfi", f"{scale}[x];[x][1:v]paletteuse=dither={dmode}:diff_mode=rectangle",
                    "-loop", "0", str(out)], check=True)
    return os.path.getsize(out) / 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("out")
    render.add_common_args(ap)
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--loop", type=float)
    ap.add_argument("--out-width", type=int)
    ap.add_argument("--max-mb", type=float, default=5.0)
    ap.add_argument("--mp4", action="store_true")
    ap.add_argument("--colors", type=int, default=192, help="palette size; 32-64 for flat two/three-colour art")
    ap.add_argument("--dither", default="bayer", help="bayer (gradients) or none (flat colour art, much smaller files)")
    a = ap.parse_args()
    src = pathlib.Path(a.html).read_text()
    m = re.search(r'<meta\s+name="gif-loop"\s+content="([\d.]+)"', src)
    loop = a.loop or (float(m.group(1)) if m else 3.0)
    tmp = render.build_html(a.html, a)
    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    frames = pathlib.Path(f"/tmp/_gif_frames_{out.stem}")
    shutil.rmtree(frames, ignore_errors=True); frames.mkdir(parents=True)

    def shoot(fps):
        for f in frames.glob("*.png"):
            f.unlink()
        n = int(round(loop * fps))
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--disable-threaded-animation", "--disable-gpu-compositing"])  # seeked frames must match what is painted
            pg = b.new_page(viewport={"width": a.width, "height": a.height})
            pg.goto(f"file://{tmp}"); pg.wait_for_timeout(600)
            clip = {"x": 0, "y": 0, "width": a.width, "height": a.height}
            for i in range(n):
                pg.evaluate(SEEK_JS, i / fps)
                pg.screenshot(path=str(frames / f"{i:04d}.png"), clip=clip)
            b.close()
        return n

    fps = a.fps
    n = shoot(fps)
    if n > 250:
        sys.exit(f"{n} frames: LinkedIn GIFs allow 250 at most; shorten the loop or lower --fps")
    widths = [w for w in [a.out_width or a.width, 960, 864, 720] if w <= (a.out_width or a.width)]
    size = None
    for w in widths:
        size = encode(frames, fps, out, w, a.colors, a.dither)
        print(f"GIF {w}px wide, {n} frames @ {fps} fps, loop {loop:g}s: {size:.2f} MB")
        if size <= a.max_mb:
            break
    if size > a.max_mb and fps > 10:
        fps = 10; n = shoot(fps)
        for w in widths:
            size = encode(frames, fps, out, w, a.colors, a.dither)
            print(f"GIF {w}px wide, {n} frames @ {fps} fps: {size:.2f} MB")
            if size <= a.max_mb:
                break
    if size > a.max_mb:
        print(f"WARN still {size:.2f} MB (limit {a.max_mb} MB): simplify the art (fewer gradients, smaller moving areas)")
    if a.mp4:
        mp4 = out.with_suffix(".mp4")
        reps = max(1, round(9 / loop))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", str(reps - 1), "-framerate", str(fps), "-i", str(frames / "%04d.png"),
                        "-vf", "format=yuv420p,setsar=1", "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", str(mp4)], check=True)
        print("saved", mp4)
    # first frame as a still for previews
    shutil.copy(frames / "0000.png", out.with_name(out.stem + "-still.png"))
    shutil.rmtree(frames, ignore_errors=True)
    print("saved", out)


if __name__ == "__main__":
    main()
