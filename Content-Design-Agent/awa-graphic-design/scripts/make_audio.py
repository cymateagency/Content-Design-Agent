#!/usr/bin/env python3
"""Synthesize an original, royalty-free soundtrack for an AWA Reel: a music bed plus timed sound effects.

Everything is generated from scratch (no samples, no third-party tracks), so AWA owns it outright.

Usage:
  python3 scripts/make_audio.py reel.html out.wav [--duration 15] [--no-music] [--no-sfx] [--music file.mp3]

Cues come from the reel template:
  <meta name="reel-sfx"   content="0.3:thud, 0.55:thud, 8.4:riser, 9.2:whoosh, 9.62:impact, 10.6:pop, 12.9:ding">
  <meta name="reel-music" content="style=drive; bpm=118; drop=9.62; key=A">

Music styles (pick to match the video's energy):
  drive    punchy house-pop: four-on-the-floor kick, offbeat bass, bright chords (default)
  chill    lo-fi: lazy swung drums, warm keys, soft bass
  hype     trap-style: half-time kick and clap, rolling hats, 808 bass
  tension  minimal pulse and dark pad before the drop, full beat after
Before the drop the bed is filtered and sparse (it teaches); at the drop it opens up (it sells).

SFX names: thud (text slam), pop (chip / pill appears), whoosh (wipe / swipe, pans left to right),
riser (build into a transition), impact (the drop / flash), ding (logo / end card), tick (counter step),
glitch (glitch-cut transition), click (UI tap).
--music mixes a licensed track under the SFX instead of the generated bed (only tracks the team has rights to).
"""
import argparse, pathlib, re, subprocess, sys
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 44100
rng = np.random.default_rng(7)


# ---------- helpers ----------
def t_(dur):
    return np.arange(int(dur * SR)) / SR


def env(n, a=0.005, d=0.2, curve=4.0):
    t = np.arange(n) / SR
    att = np.clip(t / max(a, 1e-4), 0, 1)
    return att * np.exp(-curve * np.clip(t - a, 0, None) / max(d, 1e-4))


def lp(x, fc, order=2):
    b, a = signal.butter(order, min(fc, SR / 2 - 100) / (SR / 2), "low")
    return signal.lfilter(b, a, x)


def hp(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), "high")
    return signal.lfilter(b, a, x)


def bp(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], "band")
    return signal.lfilter(b, a, x)


def saw(freq, n, detune=0.0):
    t = np.arange(n) / SR
    f = freq * (1 + detune)
    return 2 * ((t * f) % 1.0) - 1


def note(name_or_midi):
    if isinstance(name_or_midi, (int, float)):
        m = name_or_midi
    else:
        names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
        m = names[name_or_midi]
    return 440.0 * 2 ** ((m - 69) / 12)


def add(buf, x, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= buf.shape[0] or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[: buf.shape[0] - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(x), 0] += x * gain * l * 1.414
    buf[i:i + len(x), 1] += x * gain * r * 1.414


# ---------- drums ----------
def kick(dur=0.45, f0=150, f1=45, punch=1.0):
    n = int(dur * SR); t = t_(dur)
    f = f1 + (f0 - f1) * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env(n, 0.001, 0.22, 3.2)
    click = hp(rng.standard_normal(n), 3000) * env(n, 0.0005, 0.006, 6) * 0.35 * punch
    return np.tanh((body + click) * 1.6)


def clap(dur=0.3):
    n = int(dur * SR)
    nz = bp(rng.standard_normal(n), 900, 5000)
    e = np.zeros(n)
    for k, off in enumerate([0, 0.011, 0.022]):
        i = int(off * SR)
        e[i:] += env(n - i, 0.001, 0.012 if k < 2 else 0.14, 4) * (0.7 if k < 2 else 1)
    return nz * e * 0.9


def hat(dur=0.06, open_=False):
    d = 0.25 if open_ else dur
    n = int(d * SR)
    return hp(rng.standard_normal(n), 7000, 3) * env(n, 0.0005, d * 0.5, 5) * 0.5


def snare(dur=0.25):
    n = int(dur * SR); t = t_(dur)
    tone = np.sin(2 * np.pi * 190 * t) * env(n, 0.001, 0.06, 4)
    nz = bp(rng.standard_normal(n), 1500, 8000) * env(n, 0.001, 0.12, 4)
    return tone * 0.5 + nz * 0.8


def bass808(freq, dur):
    n = int(dur * SR); t = t_(dur)
    f = freq * (1 + 0.6 * np.exp(-t * 30))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return np.tanh(x * 1.8) * env(n, 0.003, dur * 0.6, 2.2)


# ---------- tonal ----------
def chord_pad(freqs, dur, bright=3000, soft=False):
    n = int(dur * SR)
    x = np.zeros(n)
    for f in freqs:
        for dt in (-0.006, 0.0, 0.007):
            x += saw(f, n, dt) * (0.6 if soft else 1.0)
    x = lp(x / (len(freqs) * 3), bright, 2)
    e = np.minimum(1, np.arange(n) / (0.08 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.12 * SR))
    return x * e


def pluck(freq, dur=0.35, bright=4000):
    n = int(dur * SR)
    x = saw(freq, n) * 0.6 + saw(freq * 2, n, 0.003) * 0.25
    return lp(x, bright) * env(n, 0.002, 0.18, 4)


def keys(freqs, dur):
    n = int(dur * SR); t = t_(dur)
    x = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) for f in freqs) / len(freqs)
    trem = 1 + 0.08 * np.sin(2 * np.pi * 4.5 * t)
    return x * trem * env(n, 0.01, dur * 0.8, 1.5)


# ---------- SFX ----------
def sfx(name):
    if name == "thud":
        k = kick(0.35, 120, 50, 0.6)
        nz = lp(rng.standard_normal(len(k)), 1800) * env(len(k), 0.001, 0.05, 5) * 0.4
        return (k * 0.8 + nz), 0.0
    if name == "pop":
        n = int(0.09 * SR); t = t_(0.09)
        f = 1400 * np.exp(-t * 18) + 500
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.03, 4) * 0.7, 0.0
    if name == "click":
        n = int(0.03 * SR)
        return hp(rng.standard_normal(n), 2500) * env(n, 0.0003, 0.004, 6) * 0.6, 0.0
    if name == "tick":
        n = int(0.05 * SR); t = t_(0.05)
        return np.sin(2 * np.pi * 2200 * t) * env(n, 0.0005, 0.01, 6) * 0.5, 0.0
    if name == "whoosh":
        d = 0.85; n = int(d * SR); t = t_(d)
        nz = rng.standard_normal(n)
        # sweep a band up then down by processing in short blocks
        out = np.zeros(n); blk = 1024
        for i in range(0, n, blk):
            p = i / n
            c = 300 + 4200 * np.sin(np.pi * p) ** 2
            seg = nz[i:i + blk]
            out[i:i + blk] = bp(seg, max(c * 0.5, 60), c * 1.6, 1)
        shape = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
        return out * shape * 1.6, "sweep"
    if name == "riser":
        d = 0.9; n = int(d * SR); t = t_(d)
        f = 200 * (2 ** (t / d * 3))
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
        nz = hp(rng.standard_normal(n), 2000) * 0.5
        shape = (t / d) ** 2.2
        return (tone + nz) * shape, 0.0
    if name == "impact":
        d = 1.4; n = int(d * SR); t = t_(d)
        boom = np.sin(2 * np.pi * np.cumsum(40 + 90 * np.exp(-t * 12)) / SR) * env(n, 0.001, 0.7, 2.5)
        crack = lp(rng.standard_normal(n), 6000) * env(n, 0.0005, 0.08, 4) * 0.6
        tail = lp(rng.standard_normal(n), 1200) * env(n, 0.01, 0.9, 2.5) * 0.15
        return np.tanh((boom * 1.3 + crack + tail) * 1.3), 0.0
    if name == "ding":
        d = 1.6; n = int(d * SR); t = t_(d)
        x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * dcy) for f, a, dcy in
                [(1318.5, 1, 2.2), (2637, .35, 3.5), (3951, .15, 5), (1975.5, .25, 3)])
        return x * 0.45 * np.minimum(1, t / 0.002), 0.0
    if name == "glitch":
        d = 0.32; n = int(d * SR)
        x = np.zeros(n)
        for i in range(0, n, int(0.02 * SR)):
            seg = int(0.012 * SR)
            f = rng.choice([180, 420, 900, 2400])
            x[i:i + seg] = signal.square(2 * np.pi * f * t_(seg / SR))[: len(x[i:i + seg])] * 0.35
        return lp(x, 5000), 0.0
    raise SystemExit(f"unknown sfx: {name}")


# ---------- music ----------
PROG = {  # semitone offsets from key root (minor key): i - VI - III - VII
    "i": [0, 3, 7], "VI": [-4, 0, 3], "III": [3, 7, 10], "VII": [-2, 2, 5]}
ORDER = ["i", "VI", "III", "VII"]
KEYS = {"C": 48, "C#": 49, "D": 50, "D#": 51, "E": 52, "F": 53, "F#": 54, "G": 55, "G#": 56, "A": 57, "A#": 58, "B": 59}


def music(dur, style="drive", bpm=118, drop=None, key="A"):
    buf = np.zeros((int(dur * SR) + SR, 2))
    beat = 60 / bpm
    bar = beat * 4
    drop = drop if drop is not None else dur * 0.6
    root = KEYS.get(key, 57)
    nbars = int(np.ceil(dur / bar)) + 1
    duck = np.ones(buf.shape[0])  # sidechain envelope for pads/bass

    def is_full(t):
        return t >= drop

    for b in range(nbars):
        t0 = b * bar
        ch = ORDER[b % 4]
        freqs = [note(root + s) for s in PROG[ch]]
        bassf = note(root - 12 + PROG[ch][0])
        pre = t0 + bar <= drop
        # pads: filtered before the drop, bright after
        add(buf, chord_pad(freqs, bar, bright=900 if pre else (3200 if style != "chill" else 1600),
                           soft=style == "chill"), t0, 0.22 if pre else 0.30)
        if style == "chill":
            add(buf, keys([f * 2 for f in freqs], bar), t0, 0.18)
        for s in range(16):
            t = t0 + s * beat / 4
            if t >= dur:
                break
            full = is_full(t)
            swing = beat / 4 * 0.18 if (style == "chill" and s % 2) else 0
            t += swing
            if style in ("drive", "tension"):
                if s % 4 == 0 and (full or style == "drive" and t >= drop - bar * 2):
                    add(buf, kick(), t, 0.9)
                    i = int(t * SR); m = int(0.18 * SR)
                    duck[i:i + m] = np.minimum(duck[i:i + m], 0.35 + 0.65 * np.linspace(0, 1, len(duck[i:i + m])) ** 1.5)
                if s % 8 == 4 and full:
                    add(buf, clap(), t, 0.5)
                if s % 4 == 2:
                    add(buf, hat(open_=full), t, 0.35 if full else 0.22, pan=0.2)
                if full and s % 2 == 1:
                    add(buf, hat(), t, 0.15, pan=-0.25)
                if s % 4 == 2 and (full or style == "drive"):
                    add(buf, lp(saw(bassf, int(beat / 2 * SR)), 500 if full else 280) * env(int(beat / 2 * SR), 0.003, 0.18, 2), t, 0.5)
                if style == "tension" and not full and s % 4 == 0:
                    add(buf, lp(saw(bassf, int(beat * SR)), 200) * env(int(beat * SR), 0.01, 0.4, 2), t, 0.35)
                if full and s in (0, 3, 6, 10, 12, 14):
                    add(buf, pluck(freqs[[0, 1, 2, 1, 2, 0][[0, 3, 6, 10, 12, 14].index(s)]] * 2), t, 0.13, pan=0.3 if s % 4 else -0.3)
            elif style == "hype":
                if s in (0, 10) or (full and s == 6):
                    add(buf, kick(0.5, 130, 42), t, 0.9)
                if s == 8 and full:
                    add(buf, clap(), t, 0.55)
                if full and s == 8:
                    pass
                if s % 2 == 0 or (full and s in (13, 15)):
                    add(buf, hat(0.04), t, 0.25 if full else 0.15, pan=0.15)
                if s == 0 and full:
                    add(buf, bass808(bassf / 2 if bassf > 70 else bassf, bar * 0.9), t, 0.55)
            elif style == "chill":
                if s in (0, 7, 10):
                    add(buf, kick(0.35, 110, 48, 0.4), t, 0.6 if full else 0.4)
                if s in (4, 12):
                    add(buf, snare(), t, 0.3 if full else 0.18)
                if s % 2 == 0:
                    add(buf, hat(0.05), t, 0.12, pan=0.2)
                if s in (0, 8):
                    add(buf, lp(np.sin(2 * np.pi * bassf * t_(beat * 1.8)), 400) * env(int(beat * 1.8 * SR), 0.01, 0.7, 1.5), t, 0.45)
    # apply sidechain to everything (subtle) and a lowpass sweep opening into the drop
    buf *= duck[:, None] ** 0.6
    return buf[: int(dur * SR)]


def master(buf, dur):
    n = int(dur * SR)
    buf = buf[:n]
    fade = min(int(0.8 * SR), n // 3)
    buf[-fade:] *= np.linspace(1, 0, fade)[:, None]
    buf[: int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))[:, None]
    peak = np.max(np.abs(buf)) or 1
    buf = np.tanh(buf / peak * 1.4) / np.tanh(1.4) * 0.89  # soft limit to about -1 dBFS
    return buf


def parse_meta(html, name):
    m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', html)
    return m.group(1) if m else ""


def load_track(path, dur):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-t", str(dur), "-f", "s16le", "-ac", "2",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).reshape(-1, 2).astype(np.float64) / 32768
    out = np.zeros((int(dur * SR), 2)); out[: len(x)] = x[: len(out)]
    return out


def build(html_text, dur, no_music=False, no_sfx=False, music_file=None):
    cfg = dict(kv.split("=") for kv in [p.strip() for p in parse_meta(html_text, "reel-music").split(";")] if "=" in kv)
    style = cfg.get("style", "drive")
    bpm = float(cfg.get("bpm", {"drive": 118, "chill": 84, "hype": 140, "tension": 120}.get(style, 118)))
    drop = float(cfg["drop"]) if "drop" in cfg else None
    key = cfg.get("key", "A")
    buf = np.zeros((int(dur * SR), 2))
    if not no_music:
        bed = load_track(music_file, dur) if music_file else music(dur, style, bpm, drop, key)
        bed = bed / (np.max(np.abs(bed)) or 1)
        buf += bed * (0.45 if music_file else 0.55)
    if not no_sfx:
        gains = {"thud": .55, "pop": .35, "whoosh": .7, "riser": .45, "impact": .85, "ding": .45, "tick": .3, "glitch": .4, "click": .35}
        for cue in [c.strip() for c in parse_meta(html_text, "reel-sfx").split(",") if ":" in c]:
            at, name = cue.split(":")
            x, pan = sfx(name.strip())
            at = float(at)
            if pan == "sweep":  # pan the whoosh left to right in chunks
                k = 8; L = len(x) // k
                for j in range(k):
                    add(buf, x[j * L:(j + 1) * L], at + j * L / SR, gains[name.strip()], pan=-0.8 + 1.6 * j / (k - 1))
            else:
                add(buf, x, at, gains.get(name.strip(), .5))
    return master(buf, dur), style, bpm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("out")
    ap.add_argument("--duration", type=float)
    ap.add_argument("--no-music", action="store_true"); ap.add_argument("--no-sfx", action="store_true")
    ap.add_argument("--music", help="licensed track to use instead of the generated bed")
    a = ap.parse_args()
    html = pathlib.Path(a.html).read_text()
    m = re.search(r'<meta\s+name="reel-duration"\s+content="([\d.]+)"', html)
    dur = a.duration or (float(m.group(1)) if m else 15.0)
    buf, style, bpm = build(html, dur, a.no_music, a.no_sfx, a.music)
    wavfile.write(a.out, SR, (buf * 32767).astype(np.int16))
    print(f"saved {a.out} ({dur:.1f}s, style={style}, bpm={bpm:g})")


if __name__ == "__main__":
    main()
