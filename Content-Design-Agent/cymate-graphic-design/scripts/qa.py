"""Pre-flight QA for Cymate graphics: catches the small mistakes that make a design look careless.

Called by render.py on every render (and usable on its own page object). Checks:
  - spelling of all visible text (brand and GTM terms whitelisted; add more to WORDS below)
  - typography: straight quotes or apostrophes, em dashes, double spaces, widows (one word alone on the
    last line of a headline), body text smaller than 18 px
  - layout: text closer than 56 px to the canvas edge, text blocks overlapping other text,
    near-miss alignment (left edges 1-8 px apart, which looks like a mistake rather than a choice)
  - contrast: text colour against the pixels around it (WCAG-style ratio)
Every finding prints as a WARN line. Fix them or confirm each one is deliberate.
"""
import re, subprocess, sys

WORDS = set("""cymate cymatellc cymate.io smartlead spf dkim dmarc gtm icp sdr sdrs ae aes b2b saas crm hubspot
salesforce apollo linkedin instagram youtube outbound inbound inbox inboxes warmup warmed bcc cc csv api apac emea
latam q1 q2 q3 q4 roi kpi kpis mql sql mqls sqls ceo cfo coo cmo vp vps lol lmk pov tbh asap ok okay
deliverability unsubscribe unsubscribes spam spammy spoof spoofing bounce bounced bounces bouncing booked
northwind ctrl bio intro demo demos gmail outlook emails email'd follow-up followups follow-ups email signup cta ctas abm onboarding multichannel
""".split())

QA_JS = r"""
() => {
  const root = document.body.firstElementChild;
  const R = root.getBoundingClientRect();
  const out = [], texts = [], words = [];
  const visible = el => { const s = getComputedStyle(el); return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05; };
  const transformed = el => { for (let e = el; e && e !== root; e = e.parentElement) { if (getComputedStyle(e).transform !== 'none') return true; } return false; };
  for (const el of root.querySelectorAll('*')) {
    if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue;
    if (!visible(el)) continue;
    const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim());
    if (!own.length) continue;
    // glyph box of the element's own text (not its padding or line-height box)
    const rg = document.createRange(); rg.setStartBefore(own[0]); rg.setEndAfter(own[own.length - 1]);
    const gr = rg.getBoundingClientRect(), br = el.getBoundingClientRect();
    // x from the glyphs, y clipped to the element's line boxes (tight leading is not an overlap)
    const top = Math.max(gr.top, br.top), bottom = Math.min(gr.bottom, br.bottom);
    const r = {left: gr.left, right: gr.right, width: gr.width, top, bottom, height: Math.max(0, bottom - top)};
    if (!r.width || !r.height) continue;
    const cs = getComputedStyle(el);
    const fs = parseFloat(cs.fontSize);
    const txt = own.map(n => n.textContent).join(' ').replace(/\s+/g, ' ').trim();
    words.push(el.innerText || txt);
    const label = txt.slice(0, 40);
    const boxed = [el, el.parentElement].some(e => e && (getComputedStyle(e).backgroundColor !== 'rgba(0, 0, 0, 0)' || parseFloat(getComputedStyle(e).borderLeftWidth) > 0 || getComputedStyle(e).backgroundImage !== 'none'));
    const block = !cs.display.startsWith('inline');
    texts.push({el, boxed, block, x: r.left - R.left, y: r.top - R.top, w: r.width, h: r.height, label, rot: transformed(el), ok: el.closest('[data-overlap], .ghost, [aria-hidden]') !== null,
                color: cs.color, clip: cs.webkitBackgroundClip === 'text' || cs.backgroundClip === 'text' || cs.webkitTextFillColor === 'rgba(0, 0, 0, 0)', fs});
    if (!el.closest('.sbar') && /^\s*cymate\.?\s*$/i.test(txt)) out.push('the word CYMATE is typed as text: use the official wordmark image ({{LOGO}} / {{LOGO_DARK}})');
    if (fs < 18 && !el.closest('[data-small], .sbar')) out.push(`text under 18px (${fs}px): ${label}`);
    const m = 56;
    if (!el.closest('[data-edge], .sbar, .ghost') && (r.left - R.left < m || R.right - r.right < m || r.top - R.top < m || R.bottom - r.bottom < m))
      out.push(`text within ${m}px of the edge: ${label}`);
    // widow check for display text: walk every text node in the element, find the last line
    if (fs >= 44 && !el.closest('.ghost') && !el.querySelector('br')) {
      const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let nd, tops = [];
      while ((nd = tw.nextNode())) { const t = nd.textContent; const re = /\S+/g; let mm;
        while ((mm = re.exec(t))) { const rg2 = document.createRange(); rg2.setStart(nd, mm.index); rg2.setEnd(nd, mm.index + mm[0].length); const rr = rg2.getClientRects()[0]; if (rr) tops.push(Math.round(rr.top)); } }
      if (tops.length >= 4) { const last = Math.max(...tops); const onLast = tops.filter(v => Math.abs(v - last) < 8).length;
        if (onLast === 1 && tops.some(v => v < last - 8)) out.push(`widow (one word alone on the last line): ${label}`); }
    }
  }
  // nothing may run into the brand frame (social bar, header marks)
  for (const fr of root.querySelectorAll('.sbar, .hdr-wm, .hdr-ic')) {
    if (!visible(fr)) continue;
    const f = fr.getBoundingClientRect();
    for (const t of texts) { if (fr.contains(t.el)) continue;
      const ix = Math.min(t.x + t.w, f.right - R.left) - Math.max(t.x, f.left - R.left), iy = Math.min(t.y + t.h, f.bottom - R.top) - Math.max(t.y, f.top - R.top);
      if (ix > 2 && iy > -12) out.push(`text runs into the brand frame (${fr.className.split(' ')[0]}): ${t.label}`); }
  }
  // overlaps and near-miss alignment between unrotated text blocks
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i], b = texts[j];
    if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
    const ix = Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x)), iy = Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
    const inter = ix * iy, small = Math.min(a.w * a.h, b.w * b.h);
    if (!a.ok && !b.ok && !(a.rot && b.rot) && inter > small * ((a.rot || b.rot) ? 0.35 : 0.2) && iy > Math.min(a.h, b.h) * 0.4 && !(a.x <= b.x && a.y <= b.y && a.x + a.w >= b.x + b.w && a.y + a.h >= b.y + b.h) && !(b.x <= a.x && b.y <= a.y && b.x + b.w >= a.x + a.w && b.y + b.h >= a.y + a.h))
      out.push(`text overlaps text: "${a.label}" / "${b.label}"`);
    if (!a.rot && !b.rot && a.block && b.block && !a.boxed && !b.boxed) { const d = Math.abs(a.x - b.x); if (d >= 1.5 && d <= 8 && Math.abs(a.y - b.y) < 600) out.push(`near-miss alignment (${d.toFixed(1)}px): "${a.label}" / "${b.label}"`); }
  }
  return {warnings: out, texts: texts.map(({el, ...t}) => t), words: words.join('\n')};
}
"""


def _rgb(css):
    m = re.findall(r"[\d.]+", css)
    return tuple(float(v) for v in m[:3]) if len(m) >= 3 else None


def _lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast_warnings(png_path, texts):
    from PIL import Image
    im = Image.open(png_path).convert("RGB")
    W, H = im.size
    out = []
    for t in texts:
        if t["clip"] or t["rot"]:
            continue
        col = _rgb(t["color"])
        if not col:
            continue
        pts = [(t["x"] - 6, t["y"] + t["h"] / 2), (t["x"] + t["w"] + 6, t["y"] + t["h"] / 2), (t["x"] + t["w"] / 2, t["y"] - 5), (t["x"] + t["w"] / 2, t["y"] + t["h"] + 5)]
        bgs = [im.getpixel((int(min(max(x, 0), W - 1)), int(min(max(y, 0), H - 1)))) for x, y in pts]
        bg = tuple(sorted(c[k] for c in bgs)[len(bgs) // 2] for k in range(3))
        l1, l2 = sorted([_lum(col), _lum(bg)], reverse=True)
        ratio = (l1 + 0.05) / (l2 + 0.05)
        need = 3.0 if t["fs"] >= 30 else 4.5
        if ratio < need - 0.05:
            out.append(f"low contrast {ratio:.1f}:1 (needs {need}:1): {t['label']}")
    return out


def spelling_warnings(text):
    try:
        from spellchecker import SpellChecker
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pyspellchecker", "--break-system-packages"], capture_output=True)
        try:
            from spellchecker import SpellChecker
        except ImportError:
            return ["spellcheck unavailable: proofread every word by eye"]
    sp = SpellChecker()
    out = []
    if re.search(r"[A-Za-z]'[A-Za-z]", text):
        out.append("straight apostrophe found: use ’ (curly) in on-image text")
    if re.search(r'"', text):
        out.append('straight double quotes found: use “ ” in on-image text')
    if "\u2014" in text:
        out.append("em dash found: Cymate voice uses a comma or full stop instead")
    if "  " in text:
        out.append("double space in text")
    tokens = set(re.findall(r"[A-Za-z][A-Za-z’'\-]+", text))
    for tok in tokens:
        w = tok.lower().replace("’", "'").strip("'-")
        if len(w) < 3 or w in WORDS or tok.isupper() and len(tok) <= 5:
            continue
        if not sp.unknown([w]):
            continue
        parts = [p for p in re.split(r"[-']", w) if p]
        unknown = [p for p in parts if p not in WORDS and len(p) > 2 and sp.unknown([p])] if len(parts) > 1 or "'" not in w else []
        if unknown:
            out.append(f"check spelling: {tok}")
    return sorted(out)


def blue_warnings(png_path):
    """Cymate uses no blue at all. Flag renders where visible blue (not UI icons) covers more than 0.4% of the canvas."""
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(png_path).convert("RGB").resize((270, 338))).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    blue = (b > r + 22) & (b > g + 8) & (b > 40)
    frac = blue.mean()
    return [f"blue detected on {frac*100:.1f}% of the canvas: Cymate uses no blue (check glows, gradients, photos, UI accents)"] if frac > 0.004 else []
