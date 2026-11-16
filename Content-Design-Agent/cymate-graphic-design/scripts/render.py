#!/usr/bin/env python3
"""Render a Cymate graphic HTML file to PNG (default 1080x1350).

Usage: python3 scripts/render.py poster.html out.png [--width 1080 --height 1350] [--photo p.png] [--bg photo.jpg --bg-opacity 0.25]

- Downloads the fonts from the Google Fonts GitHub repo on first run (the emoji font only when the design uses emoji).
- Inlines the shared frame: {{BASE_CSS}} (templates/_base.css), {{HEADER}} (wordmark + mascot icon),
  {{SOCIAL_BAR}} (YouTube / Instagram / LinkedIn / website pill).
- Embeds brand assets: {{LOGO}} white wordmark with orange dot, {{LOGO_DARK}} dark wordmark, {{ICON}} mascot icon
  (small), {{MASCOT}} mascot (large, for heroes and transitions), {{LOCKUP}} / {{LOCKUP_DARK}} official stacked logo
  (mascot over wordmark), {{MONOGRAM}} orange CYMATE monogram tile. Full official set: assets/brand/ (PNG + SVG).
- {{PHOTO}}: --photo path, else assets/wesley.png if bundled. {{BG}}: --bg path (a stock or team photo the user supplied).
- --bg-opacity sets --bg-op for the .tx-stock layer (allowed 0.20-0.30, default 0.25).
- Prints WARN lines for text that spills outside the canvas or overflows its box.
"""
import argparse, base64, os, pathlib, re, subprocess, sys, urllib.request

SKILL = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = pathlib.Path.home() / ".fonts"
GF = "https://raw.githubusercontent.com/google/fonts/main/"
FONTS = {
    "Poppins-Light.ttf": ("ofl/poppins/Poppins-Light.ttf", "Poppins", "normal", "300"),
    "Poppins-Regular.ttf": ("ofl/poppins/Poppins-Regular.ttf", "Poppins", "normal", "400"),
    "Poppins-Italic.ttf": ("ofl/poppins/Poppins-Italic.ttf", "Poppins", "italic", "400"),
    "Poppins-Medium.ttf": ("ofl/poppins/Poppins-Medium.ttf", "Poppins", "normal", "500"),
    "Poppins-SemiBold.ttf": ("ofl/poppins/Poppins-SemiBold.ttf", "Poppins", "normal", "600"),
    "Poppins-Bold.ttf": ("ofl/poppins/Poppins-Bold.ttf", "Poppins", "normal", "700"),
    "Poppins-ExtraBold.ttf": ("ofl/poppins/Poppins-ExtraBold.ttf", "Poppins", "normal", "800"),
    "Poppins-ExtraBoldItalic.ttf": ("ofl/poppins/Poppins-ExtraBoldItalic.ttf", "Poppins", "italic", "800"),
    "Poppins-Black.ttf": ("ofl/poppins/Poppins-Black.ttf", "Poppins", "normal", "900"),
    "Inter.ttf": ("ofl/inter/Inter%5Bopsz,wght%5D.ttf", "Inter", "normal", "100 900"),
    "BalooThambi2.ttf": ("ofl/baloothambi2/BalooThambi2%5Bwght%5D.ttf", "Baloo Thambi 2", "normal", "400 800"),
    "Bungee-Regular.ttf": ("ofl/bungee/Bungee-Regular.ttf", "Bungee", "normal", "400"),
    "Anton-Regular.ttf": ("ofl/anton/Anton-Regular.ttf", "Anton", "normal", "400"),
    "LuckiestGuy-Regular.ttf": ("apache/luckiestguy/LuckiestGuy-Regular.ttf", "Luckiest Guy", "normal", "400"),
    "RubikDirt-Regular.ttf": ("ofl/rubikdirt/RubikDirt-Regular.ttf", "Rubik Dirt", "normal", "400"),
    "ArchivoBlack-Regular.ttf": ("ofl/archivoblack/ArchivoBlack-Regular.ttf", "Archivo Black", "normal", "400"),
    "SpaceGrotesk.ttf": ("ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf", "Space Grotesk", "normal", "300 700"),
    "Unbounded.ttf": ("ofl/unbounded/Unbounded%5Bwght%5D.ttf", "Unbounded", "normal", "200 900"),
    "InstrumentSerif-Italic.ttf": ("ofl/instrumentserif/InstrumentSerif-Italic.ttf", "Instrument Serif", "italic", "400"),
    "InstrumentSerif-Regular.ttf": ("ofl/instrumentserif/InstrumentSerif-Regular.ttf", "Instrument Serif", "normal", "400"),
    "BebasNeue-Regular.ttf": ("ofl/bebasneue/BebasNeue-Regular.ttf", "Bebas Neue", "normal", "400"),
    "Caveat.ttf": ("ofl/caveat/Caveat%5Bwght%5D.ttf", "Caveat", "normal", "400 700"),
    "PermanentMarker-Regular.ttf": ("apache/permanentmarker/PermanentMarker-Regular.ttf", "Permanent Marker", "normal", "400"),
    "IBMPlexMono-Regular.ttf": ("ofl/ibmplexmono/IBMPlexMono-Regular.ttf", "IBM Plex Mono", "normal", "400"),
    "IBMPlexMono-SemiBold.ttf": ("ofl/ibmplexmono/IBMPlexMono-SemiBold.ttf", "IBM Plex Mono", "normal", "600"),
}
EMOJI = ("NotoColorEmoji-Regular.ttf", "ofl/notocoloremoji/NotoColorEmoji-Regular.ttf")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def ensure_fonts(need_emoji=False):
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    faces = []
    if need_emoji:
        dest = FONT_DIR / EMOJI[0]
        if not dest.exists():
            try:
                urllib.request.urlretrieve(GF + EMOJI[1], dest)
            except Exception as e:
                print(f"WARN emoji font download failed ({e})")
        if dest.exists():
            faces.append(f"@font-face{{font-family:'Noto Color Emoji';src:url('file://{dest}')}}")
    for fname, (path, family, style, weight) in FONTS.items():
        dest = FONT_DIR / fname
        if not dest.exists():
            try:
                urllib.request.urlretrieve(GF + path, dest)
            except Exception as e:  # keep going; the check below reports it
                print(f"WARN font download failed: {fname} ({e})")
                continue
        faces.append(
            f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};src:url('file://{dest}')}}"
        )
    return "\n".join(faces)


def data_uri(p, mime):
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml"}


def asset(path_arg, default):
    p = pathlib.Path(path_arg) if path_arg else SKILL / "assets" / default
    if not p.exists():
        sys.exit(f"missing asset: {p}")
    return data_uri(p, MIME.get(p.suffix.lower(), "image/png"))


def partial(name):
    return (SKILL / "templates" / name).read_text()


def ensure_playwright():
    try:
        import playwright  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "--break-system-packages", "-q"], check=False)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch().close()
    except Exception:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)


CHECK_JS = """
() => {
  const root = document.body.firstElementChild;
  const R = root.getBoundingClientRect();
  const out = [];
  for (const el of root.querySelectorAll('*')) {
    if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const txt = (el.innerText || el.getAttribute('aria-label') || el.tagName).trim().slice(0, 40);
    const isText = el.childNodes && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (isText && (r.left < R.left - 1 || r.right > R.right + 1 || r.top < R.top - 1 || r.bottom > R.bottom + 1))
      out.push('outside poster: ' + txt);
    if (isText && el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow !== 'visible')
      out.push('text overflows its box: ' + txt);
  }
  return out;
}
"""


ASSETS = [("{{LOGO}}", "logo", "wordmark-white.png"), ("{{LOGO_DARK}}", "logo_dark", "wordmark-dark.png"),
          ("{{ICON}}", "icon", "mascot-icon.png"), ("{{MASCOT}}", "mascot", "mascot-large.png"),
          ("{{LOCKUP}}", "lockup", "logo-lockup-white.png"), ("{{LOCKUP_DARK}}", "lockup_dark", "logo-lockup-dark.png"),
          ("{{MONOGRAM}}", "monogram", "monogram.png")]


def add_common_args(ap):
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--logo", help="override the white wordmark ({{LOGO}})")
    ap.add_argument("--logo-dark", help="override the dark wordmark ({{LOGO_DARK}})")
    ap.add_argument("--icon", help="override the small mascot icon ({{ICON}})")
    ap.add_argument("--mascot", help="override the large mascot ({{MASCOT}})")
    ap.add_argument("--lockup", help="override the stacked logo ({{LOCKUP}})")
    ap.add_argument("--lockup-dark", help="override the dark stacked logo ({{LOCKUP_DARK}})")
    ap.add_argument("--monogram", help="override the CYMATE monogram tile ({{MONOGRAM}})")
    ap.add_argument("--photo", help="photo for {{PHOTO}}, e.g. a Wesley cutout PNG the user supplied")
    ap.add_argument("--bg", help="background image for {{BG}} (stock or team photo the user supplied)")
    ap.add_argument("--bg-opacity", type=float, default=0.25, help="opacity of the .tx-stock layer, 0.20-0.30")
    ap.add_argument("--raw", action="store_true", help="skip the Photoshop-style finishing pass (finish.py)")
    ap.add_argument("--finish", type=float, default=1.0, help="finishing strength (0.6 quieter, 1.3 more filmic)")
    ap.add_argument("--scale", type=int, default=2, help="supersampling factor: render at Nx, downsample to the final size")


def build_html(src, a, extra_css=""):
    """Inline partials, fonts and assets; return the path of a ready-to-load HTML file."""
    html = pathlib.Path(src).read_text()
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)  # template notes never reach the render
    html = html.replace("{{BASE_CSS}}", "<style>" + partial("_base.css") + "</style>")
    html = html.replace("{{HEADER}}", partial("_header.html"))
    html = html.replace("{{SOCIAL_BAR}}", partial("_socialbar.html"))
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)

    faces = ensure_fonts(bool(EMOJI_RE.search(html)))
    ensure_playwright()
    for tag, attr, default in ASSETS:
        if tag in html:
            html = html.replace(tag, asset(getattr(a, attr, None), default))
    if "{{PHOTO}}" in html:
        if not a.photo and not (SKILL / "assets/wesley.png").exists():
            sys.exit("this template needs --photo (a photo the user supplied, e.g. a Wesley cutout PNG)")
        html = html.replace("{{PHOTO}}", asset(a.photo, "wesley.png"))
    if "{{BG}}" in html:
        if not a.bg:
            sys.exit("this template needs --bg (a background image the user supplied)")
        html = html.replace("{{BG}}", asset(a.bg, ""))
    op = a.bg_opacity
    if not 0.20 <= op <= 0.30:
        print(f"WARN --bg-opacity {op} is outside 0.20-0.30; clamped")
        op = min(max(op, 0.20), 0.30)
    html = html.replace("</head>", f"<style>{faces}\nbody{{margin:0}}\n:root{{--bg-op:{op}}}\n{extra_css}</style></head>", 1)
    tmp = pathlib.Path(f"/tmp/_cymate_render_{os.getpid()}.html")
    tmp.write_text(html)
    return tmp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    add_common_args(ap)
    a = ap.parse_args()
    tmp = build_html(a.html, a)
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import qa
    from playwright.sync_api import sync_playwright

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    big = a.out + ".hi.png"
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--disable-threaded-animation", "--disable-gpu-compositing"])  # seeked frames must match what is painted
        # Supersample: render at 2x and downsample with Lanczos, like a careful Photoshop export.
        pg = b.new_page(viewport={"width": a.width, "height": a.height}, device_scale_factor=a.scale)
        pg.goto(f"file://{tmp}")
        pg.wait_for_timeout(500)
        # Animated templates: freeze every animation at the still time so the PNG shows the finished state.
        m = re.search(r'<meta\s+name="still-time"\s+content="([\d.]+)"', pathlib.Path(a.html).read_text())
        still = float(m.group(1)) if m else 4.0
        pg.evaluate("async (t) => { for (const an of document.getAnimations()) { an.pause(); an.currentTime = t * 1000; } await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }", still)
        pg.wait_for_timeout(50)
        warns = list(pg.evaluate(CHECK_JS))
        res = pg.evaluate(qa.QA_JS)
        pg.screenshot(path=big, clip={"x": 0, "y": 0, "width": a.width, "height": a.height})
        paper = pg.evaluate("() => !!document.querySelector('.cm.paper, .cm.light')")
        b.close()
    from PIL import Image
    im = Image.open(big).convert("RGB")
    if im.size != (a.width, a.height):
        im = im.resize((a.width, a.height), Image.LANCZOS)
    if not a.raw:
        import finish
        im = finish.finish(im, a.finish, paper)
    im.save(a.out, optimize=True)
    os.remove(big)
    warns += res["warnings"] + qa.contrast_warnings(a.out, res["texts"]) + qa.spelling_warnings(res["words"]) + qa.blue_warnings(a.out)
    for w in dict.fromkeys(warns):
        print("WARN", w)
    print("saved", a.out, "(raw)" if a.raw else "(finished)")


if __name__ == "__main__":
    main()
