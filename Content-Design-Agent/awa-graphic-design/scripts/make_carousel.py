#!/usr/bin/env python3
"""Render a folder of carousel slide HTML files and join them into one LinkedIn-ready PDF.

Usage: python3 scripts/make_carousel.py slides_dir/ out/carousel-name.pdf [--video] [--music] [--logo path ...]

--video (on request; static carousels are the AWA default): also renders every slide to an animated 1080x1350 MP4
  (carousel-name-01.mp4, ...) with make_reel.py, using each slide's motion classes, reel-duration and
  reel-sfx cues. Slides get sound effects only, no music bed: Instagram plays one music track across the
  whole carousel when it's added in-app, and a bed baked into each slide would restart on every swipe.
--music: bake the generated music bed into each slide as well (only if asked).

Any extra flags (--logo, --logo-dark, --logo-white, --photo) are passed through to render.py.

- Renders every *.html in slides_dir in name order (01.html, 02.html, ...) with render.py,
  so fonts, logos and the overflow warnings work exactly as for posters.
- Saves each slide PNG next to the PDF (carousel-name-01.png, ...) so you can view and fix them.
"""
import pathlib, subprocess, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    rest = sys.argv[3:]
    video = "--video" in rest
    music = "--music" in rest
    rest = [r for r in rest if r not in ("--video", "--music")]
    slides = sorted(src.glob("*.html"))
    if not slides:
        sys.exit(f"no .html slides in {src}")
    out.parent.mkdir(parents=True, exist_ok=True)
    pngs = []
    for i, s in enumerate(slides, 1):
        png = out.with_name(f"{out.stem}-{i:02d}.png")
        print(f"slide {i}: {s.name}")
        subprocess.run([sys.executable, str(HERE / "render.py"), str(s), str(png)] + rest, check=True)
        pngs.append(png)
        if video:
            mp4 = out.with_name(f"{out.stem}-{i:02d}.mp4")
            cmd = [sys.executable, str(HERE / "make_reel.py"), str(s), str(mp4), "--width", "1080", "--height", "1350"] + rest
            if not music:
                cmd.append("--no-music")
            subprocess.run(cmd, check=True)
            mp4.with_name(mp4.stem + "-cover.png").unlink(missing_ok=True)
            # The MP4 must match the PNG exactly (same canvas on Instagram, mixed photo/video carousels).
            dims = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height", "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout.strip()
            pw, ph = Image.open(png).size
            if dims != f"{pw},{ph}":
                sys.exit(f"size mismatch on slide {i}: MP4 {dims} vs PNG {pw}x{ph}")
            print(f"slide {i}: MP4 and PNG both {pw}x{ph}")
    imgs = [Image.open(p).convert("RGB") for p in pngs]
    imgs[0].save(out, save_all=True, append_images=imgs[1:], resolution=144)
    print(f"saved {out} ({len(imgs)} slides)")


if __name__ == "__main__":
    main()
