#!/usr/bin/env python3
"""Render an AWA (Agency Workplaces) graphic HTML file to PNG (default 1080x1350).

Usage: python3 scripts/render.py poster.html out.png [--width 1080 --height 1350] [--photo p.png] [--bg photo.jpg --bg-opacity 0.25]

- Downloads the AWA fonts (Poppins, Anton, Caveat) from the Google Fonts GitHub repo on first run.
- Inlines the shared frame: {{BASE_CSS}} (templates/_base.css) and {{HEADER}} (AWA logo, swaps by background).
  AWA posts carry the logo only: there is no social bar.
- Embeds the AWA logo: {{LOGO}} light version (red mark, white words) for black/dark/photo backgrounds,
  {{LOGO_DARK}} (red mark, black words) for white backgrounds, {{LOGO_WHITE}} (all white) for red backgrounds.
  Official files (PNG + SVG): assets/brand/.
- {{PHOTO}}: --photo path (a photo the user supplied, ideally a transparent cut-out PNG). {{BG}}: --bg path.
- --bg-opacity sets --bg-op for the .tx-stock layer (allowed 0.20-0.30, default 0.25).
- Prints WARN lines for text that spills outside the canvas or overflows its box, plus the qa.py checks.
"""
import argparse, base64, os, pathlib, re, subprocess, sys, urllib.request

SKILL = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = pathlib.Path.home() / ".fonts"
GF = "https://raw.githubusercontent.com/google/fonts/main/"
FONTS = {  # AWA fonts: Poppins (default), Anton (statement headlines), Caveat (handwritten notes)
    "Poppins-Light.ttf": ("ofl/poppins/Poppins-Light.ttf", "Poppins", "normal", "300"),
    "Poppins-LightItalic.ttf": ("ofl/poppins/Poppins-LightItalic.ttf", "Poppins", "italic", "300"),
    "Poppins-Regular.ttf": ("ofl/poppins/Poppins-Regular.ttf", "Poppins", "normal", "400"),
    "Poppins-Italic.ttf": ("ofl/poppins/Poppins-Italic.ttf", "Poppins", "italic", "400"),
    "Poppins-Medium.ttf": ("ofl/poppins/Poppins-Medium.ttf", "Poppins", "normal", "500"),
    "Poppins-SemiBold.ttf": ("ofl/poppins/Poppins-SemiBold.ttf", "Poppins", "normal", "600"),
    "Poppins-SemiBoldItalic.ttf": ("ofl/poppins/Poppins-SemiBoldItalic.ttf", "Poppins", "italic", "600"),
    "Poppins-Bold.ttf": ("ofl/poppins/Poppins-Bold.ttf", "Poppins", "normal", "700"),
    "Poppins-ExtraBold.ttf": ("ofl/poppins/Poppins-ExtraBold.ttf", "Poppins", "normal", "800"),
    "Poppins-ExtraBoldItalic.ttf": ("ofl/poppins/Poppins-ExtraBoldItalic.ttf", "Poppins", "italic", "800"),
    "Poppins-Black.ttf": ("ofl/poppins/Poppins-Black.ttf", "Poppins", "normal", "900"),
    "Anton-Regular.ttf": ("ofl/anton/Anton-Regular.ttf", "Anton", "normal", "400"),
    "Caveat.ttf": ("ofl/caveat/Caveat%5Bwght%5D.ttf", "Caveat", "normal", "400 700"),
}


def ensure_fonts():
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    faces = []
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
  // Seamless carousels (data-panorama): text that sits wholly on another slide of the shared canvas is not on this one.
  const pano = root.hasAttribute('data-panorama');
  for (const el of root.querySelectorAll('*')) {
    if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue;
    if (el.closest('[aria-hidden], .ghost, [data-edge]')) continue;  // ghost words and deliberate edge-crossers
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (pano && (r.right <= R.left || r.left >= R.right)) continue;
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


ASSETS = [("{{LOGO}}", "logo", "logo-light.png"), ("{{LOGO_DARK}}", "logo_dark", "logo-dark.png"),
          ("{{LOGO_WHITE}}", "logo_white", "logo-white.png")]


def add_common_args(ap):
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--logo", help="override the light logo, white words ({{LOGO}})")
    ap.add_argument("--logo-dark", help="override the dark logo, black words ({{LOGO_DARK}})")
    ap.add_argument("--logo-white", help="override the all-white logo ({{LOGO_WHITE}})")
    ap.add_argument("--photo", help="photo for {{PHOTO}}: a photo the user supplied (cut-out PNG works best)")
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
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)

    faces = ensure_fonts()
    ensure_playwright()
    for tag, attr, default in ASSETS:
        if tag in html:
            html = html.replace(tag, asset(getattr(a, attr, None), default))
    if "{{PHOTO}}" in html:
        if not a.photo:
            sys.exit("this template needs --photo (a real photo the user supplied; never generate people)")
        html = html.replace("{{PHOTO}}", asset(a.photo, ""))
    if "{{BG}}" in html:
        if not a.bg:
            sys.exit("this template needs --bg (a background image the user supplied)")
        html = html.replace("{{BG}}", asset(a.bg, ""))
    op = a.bg_opacity
    if not 0.20 <= op <= 0.30:
        print(f"WARN --bg-opacity {op} is outside 0.20-0.30; clamped")
        op = min(max(op, 0.20), 0.30)
    html = html.replace("</head>", f"<style>{faces}\nbody{{margin:0}}\n:root{{--bg-op:{op}}}\n{extra_css}</style></head>", 1)
    tmp = pathlib.Path(f"/tmp/_awa_render_{os.getpid()}.html")
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
        paper = pg.evaluate("() => !!document.querySelector('.aw.white')")
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
    warns += res["warnings"] + qa.contrast_warnings(a.out, res["texts"]) + qa.spelling_warnings(res["words"]) + qa.palette_warnings(a.out)
    for w in dict.fromkeys(warns):
        print("WARN", w)
    print("saved", a.out, "(raw)" if a.raw else "(finished)")


if __name__ == "__main__":
    main()
