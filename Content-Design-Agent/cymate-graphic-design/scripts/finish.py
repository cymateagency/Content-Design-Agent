#!/usr/bin/env python3
"""Photoshop-style finishing pass for a rendered Cymate graphic.

A raw browser render is mathematically clean: flat gradients that band, perfectly uniform darks, no lens,
no grain. That cleanliness is what reads as "generated". This pass does what a designer does in Photoshop
before export, all subtle enough that nobody should notice any single step:

  1. Gentle S-curve (Curves) for depth in the mid-tones.
  2. Split toning: neutral-warm shadows, warm highlights (no blue cast anywhere).
  3. Light bloom: bright and orange areas softly glow into their surroundings (Screen blend).
  4. Lens vignette: corners fall off a few percent, pulling the eye to the centre.
  5. Smart sharpen on edges only (text and UI stay crisp after downsampling).
  6. Luminance-aware film grain: monochrome, strongest in mid-tones, near zero in pure black and white.
     It also dithers gradients so they never band on Instagram's compression.

Usage:
  python3 scripts/finish.py in.png out.png [--strength 1.0] [--paper]
render.py calls this automatically (skip with --raw). --paper lightens the vignette and grain for
off-white backgrounds. Strength scales every step (0.6 = quieter, 1.3 = more filmic).
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def finish(img, strength=1.0, paper=False, seed=11):
    img = img.convert("RGB")
    rgb = np.asarray(img).astype(np.float32) / 255.0
    h, w, _ = rgb.shape
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    s = strength

    # 1. Curves: soft S around mid-grey, 12% blend
    sc = rgb + (smoothstep(0, 1, rgb) - rgb) * 0.12 * s
    rgb = np.clip(sc, 0, 1)

    # 2. Split toning
    sh = (1 - smoothstep(0.0, 0.35, lum))[..., None]
    hi = smoothstep(0.6, 1.0, lum)[..., None]
    rgb = rgb + sh * np.array([0.004, 0.001, -0.003], np.float32) * s
    rgb = rgb + hi * np.array([0.012, 0.004, -0.008], np.float32) * s

    # 3. Bloom from bright or strongly orange pixels
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    orange = np.clip((r - b) * 1.4 - 0.35, 0, 1) * (r > 0.6)
    bright = smoothstep(0.78, 1.0, lum)
    src = (np.maximum(orange, bright * (0.5 if paper else 1.0)))[..., None] * rgb
    src_img = Image.fromarray((np.clip(src, 0, 1) * 255).astype(np.uint8))
    glow = np.asarray(src_img.filter(ImageFilter.GaussianBlur(22))).astype(np.float32) / 255.0
    amt = (0.10 if paper else 0.20) * s
    rgb = 1 - (1 - rgb) * (1 - glow * amt)  # screen

    # 4. Vignette
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / np.sqrt(2)
    vig = 1 - smoothstep(0.45, 1.0, d) * (0.05 if paper else 0.12) * s
    rgb = rgb * vig[..., None]

    out = Image.fromarray((np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8))

    # 5. Smart sharpen (edges only via threshold)
    out = out.filter(ImageFilter.UnsharpMask(radius=1.1, percent=int(35 * s), threshold=3))

    # 6. Luminance-aware monochrome grain (also dithers gradients)
    rgb = np.asarray(out).astype(np.float32) / 255.0
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (h, w)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.55))).astype(np.float32)
    n = (n - 128) / 40
    mid = 0.35 + 2.2 * lum * (1 - lum)  # some grain even in darks, most in mid-tones
    grain = n * mid * (0.010 if paper else 0.016) * s
    rgb = rgb + grain[..., None]
    return Image.fromarray((np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--strength", type=float, default=1.0)
    ap.add_argument("--paper", action="store_true")
    a = ap.parse_args()
    finish(Image.open(a.src), a.strength, a.paper).save(a.out, optimize=True)
    print("finished", a.out)


if __name__ == "__main__":
    main()
