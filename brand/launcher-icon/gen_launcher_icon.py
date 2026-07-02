#!/usr/bin/env python3
"""
Hora-family launcher-icon engine (FINAL).

The family icon is a Malayalam wordmark (Pathivu "പതി", Varisankya "വരി") set in
**Baloo Chettan 2** (rounded, OFL) in slate on near-white, centered, sized to a fixed
bounding circle. Rendering uses harfbuzz (shaping) + FreeType (the font's own nonzero
rasterizer — no fill-rule holes), so edges are crisp and the ത/പ counters are correct.

One algorithm, both apps: pass a different `text` (and res dir). Run from anywhere.
Deps: uharfbuzz, freetype-py, fontTools (woff2->ttf), numpy, Pillow.
"""
import os, math
import numpy as np
import uharfbuzz as hb
import freetype
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

# ---- Family standard (locked with Aarsh, 2026-06) --------------------------
FONT      = os.path.join(FONTS, "BalooChettan2-700.ttf")  # Baloo Chettan 2, weight 700
SLATE     = (0x44, 0x53, 0x53)
BG        = (0xFC, 0xFC, 0xFC)
YSTRETCH  = 1.45     # vertical stretch ("taller")
EM        = 2000     # FreeType em pixels (hi-res master for crisp downsamples)

# ---- Icon sizing standard (the established family look; matches Pathivu/Varisankya) ---
# THE RULE: the wordmark is scaled so its *circumscribing circle* (the smallest circle,
# centred on the canvas, that exactly contains the wordmark's bounding box) has radius
# `r_frac * canvas`. `r_frac` is therefore exactly *circle radius / canvas*, and is
# aspect-independent (render() solves th/tw so circ_r == r_frac*canvas regardless of the
# wordmark's proportions). Each surface has its own `r_frac`, chosen so every Hora app's
# icons look identical across the family. These values are the ones Pathivu and Varisankya
# actually ship (measured off their committed assets) — the single source of truth. An
# earlier "fill the safe circle" experiment (FULL=0.5 / FG=0.305 / MASK=0.40) was applied
# to one app only and read as oversized/edge-touching; reverted to these per-surface values
# so the whole family matches (confirmed with Aarsh, 2026-07).
# Since 2026-07-02 the r_frac circle circumscribes the (ink width × BASE-LETTER BAND
# height) box — NOT the full ink box (see "band rule" below). Constants were
# re-calibrated from the previous full-ink values by ×0.9329 (the Pathivu band/full
# diagonal ratio) so Pathivu's rendered base-letter size is unchanged; every app's
# BASE LETTERS now render at the same size and sit on the same optical line, with
# ascenders (ീ/ി) and descenders (ു) extending beyond the band.
#   PLAY_RFRAC     (0.3825) — Play Store 512 listing icon. Smaller than full-bleed because
#                             Play re-crops + shadow-frames it in its own grid/detail chrome.
#   FLAT_RFRAC     (0.2799) — flat square icons: iOS AppIcon + web favicon / PWA "any" icons.
#   LAUNCHER_RFRAC (0.3200) — Android legacy + round launcher (full-bleed slate-on-BG square).
#   FG_RFRAC       (0.2295) — Android adaptive foreground + monochrome (full ink hard-capped
#                             to the 66dp/108dp adaptive safe circle, 0.305).
#   MASK_RFRAC     (0.2239) — maskable web icon (full ink hard-capped to the W3C 0.40 zone).
PLAY_RFRAC     = 0.3825
FLAT_RFRAC     = 0.2799
LAUNCHER_RFRAC = 0.3200
FG_RFRAC       = 0.2295
MASK_RFRAC     = 0.2239
FG_SAFE_HARD   = 0.305   # adaptive-icon safe circle — full ink must never exceed this
MASK_SAFE_HARD = 0.40    # W3C maskable safe circle — full ink must never exceed this
R_FRAC         = FLAT_RFRAC   # back-compat default for bare render() calls

def wordmark_mask_with_baseline(text, font=FONT, ystretch=YSTRETCH):
    """Alpha mask of the shaped, FreeType-rasterised wordmark, vertically stretched,
    cropped to ink — plus the BASELINE row inside the cropped mask (float). The
    baseline is what lets the band rule locate the base-letter band regardless of
    ascenders (ീ/ി) or descenders (ു) in the wordmark."""
    ft = freetype.Face(font); upem = ft.units_per_EM; ft.set_pixel_sizes(0, EM)
    hbf = hb.Font(hb.Face(hb.Blob.from_file_path(font)))
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(hbf, buf)
    sc = EM / upem; penx = 0.0; items = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        ft.load_glyph(info.codepoint, freetype.FT_LOAD_RENDER)
        b = ft.glyph.bitmap; r, w, p = b.rows, b.width, b.pitch
        a = np.array(b.buffer, np.uint8).reshape(r, p)[:, :w] if r > 0 else np.zeros((0, 0), np.uint8)
        items.append((penx + pos.x_offset*sc + ft.glyph.bitmap_left,
                      -(pos.y_offset*sc) - ft.glyph.bitmap_top, a))
        penx += pos.x_advance * sc
    items = [(x, y, a) for x, y, a in items if a.size]
    minx = min(int(math.floor(x)) for x, _, _ in items); miny = min(int(math.floor(y)) for _, y, _ in items)
    maxx = max(int(math.ceil(x)) + a.shape[1] for x, _, a in items); maxy = max(int(math.ceil(y)) + a.shape[0] for _, y, a in items)
    cv = Image.new("L", (maxx-minx, maxy-miny), 0)
    for x, y, a in items:
        px = int(round(x-minx)); py = int(round(y-miny)); gi = Image.fromarray(a)
        reg = cv.crop((px, py, px+a.shape[1], py+a.shape[0])); cv.paste(ImageChops.lighter(reg, gi), (px, py))
    baseline = float(-miny)                      # glyph y's are baseline-relative; row 0 = miny
    if ystretch != 1.0:
        cv = cv.resize((cv.width, int(round(cv.height*ystretch))), Image.LANCZOS)
        baseline *= ystretch
    l, t, r, b = cv.getbbox()
    return cv.crop((l, t, r, b)), baseline - t

def wordmark_mask(text, font=FONT, ystretch=YSTRETCH):
    """Back-compat: mask only."""
    return wordmark_mask_with_baseline(text, font, ystretch)[0]

# ---- Base-letter band (THE band rule, locked with Aarsh 2026-07-02) ----------
# Malayalam vowel signs break naive bbox fitting: ു (Muthal "മുത") descends BELOW the
# base letters while ീ/ി (Pathivu "പതി", Varisankya "വരി") ascend ABOVE them — so
# fitting the full ink box makes the *base letters* render at different sizes and
# different vertical positions per app. The fix: all scaling and centering is done on
# the BASE-LETTER BAND — the ink band of a plain base consonant (they all share the
# same band in Baloo Chettan 2: പ/മ/വ/ത ≈ equal height, sitting on the baseline).
# Ascenders/descenders simply extend beyond the band. REF_BAND_GLYPH defines the band
# once, family-wide.
REF_BAND_GLYPH = "പ"   # പ

_band_cache = None
def _band():
    """(band_h, band_top_rel) — band height and its top relative to the baseline
    (negative = above), measured through the identical shaping/stretch pipeline."""
    global _band_cache
    if _band_cache is None:
        ref, ref_base = wordmark_mask_with_baseline(REF_BAND_GLYPH)
        _band_cache = (float(ref.height), -ref_base)
    return _band_cache

def render(text, canvas_px, color, r_frac=R_FRAC, bg=None, circle=False, ss=4, hard_rfrac=0.5):
    """Wordmark rendered under the BAND rule: the circle of radius r_frac*canvas
    circumscribes the box (full ink width × base-letter band height), and the BAND's
    vertical centre sits on the canvas centre. Ascenders/descenders extend beyond the
    band; `hard_rfrac` is a safety clamp — if the FULL ink would poke outside that
    circle (e.g. the adaptive-icon safe zone), the whole wordmark scales down to fit,
    band stays centred. Optional bg / circle mask as before."""
    S = canvas_px * ss
    m, base = wordmark_mask_with_baseline(text); w, h = m.size
    band_h, band_top_rel = _band()
    band_center = base + band_top_rel + band_h / 2.0        # row of band centre in mask
    R = r_frac * S
    s = 2.0 * R / math.hypot(w, band_h)
    # Safety clamp on the FULL ink box (corner farthest from the canvas centre).
    d_top = abs(0 - band_center); d_bot = abs(h - band_center)
    dmax = max(math.hypot(w / 2.0, d_top), math.hypot(w / 2.0, d_bot))
    if s * dmax > hard_rfrac * S:
        s = hard_rfrac * S / dmax
    tw = max(1, round(w * s)); th = max(1, round(h * s))
    m = m.resize((tw, th), Image.LANCZOS)
    alpha = Image.new("L", (S, S), 0)
    alpha.paste(m, ((S - tw) // 2, round(S / 2.0 - band_center * s)))
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    if bg is not None:
        if circle:
            mk = Image.new("L", (S, S), 0); ImageDraw.Draw(mk).ellipse([0, 0, S-1, S-1], fill=255)
            img = Image.composite(Image.new("RGBA", (S, S), bg + (255,)), img, mk)
        else:
            img = Image.new("RGBA", (S, S), bg + (255,))
    tile = Image.new("RGBA", (S, S), color + (0,)); tile.putalpha(alpha)
    img.alpha_composite(tile)
    return img.resize((canvas_px, canvas_px), Image.LANCZOS)

def _save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True); img.save(path, "PNG")

FG = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}
LG = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}

def generate(text, res_dir):
    """Write the full Android asset set for `text` into `res_dir`."""
    for dpi, px in FG.items():
        _save(render(text, px, SLATE, r_frac=FG_RFRAC, hard_rfrac=FG_SAFE_HARD),
              os.path.join(res_dir, f"mipmap-{dpi}", "ic_launcher_foreground.png"))
    _save(render(text, 432, (0, 0, 0), r_frac=FG_RFRAC, hard_rfrac=FG_SAFE_HARD),
          os.path.join(res_dir, "drawable-nodpi", "ic_launcher_monochrome.png"))
    for dpi, px in LG.items():
        _save(render(text, px, SLATE, r_frac=LAUNCHER_RFRAC, bg=BG).convert("RGB"),
              os.path.join(res_dir, f"mipmap-{dpi}", "ic_launcher.png"))
        _save(render(text, px, SLATE, r_frac=LAUNCHER_RFRAC, bg=BG, circle=True),
              os.path.join(res_dir, f"mipmap-{dpi}", "ic_launcher_round.png"))

def play_icon(text, out_path):
    """Play Store 512 listing icon (full-bleed square). Wordmark maxed inside the smaller
    PLAY_RFRAC circle (not the full canvas) so it doesn't read as cramped inside Play's
    own grid/detail chrome — the established family look. Write OUTSIDE res/ (not a build
    resource)."""
    _save(render(text, 512, SLATE, r_frac=PLAY_RFRAC, bg=BG).convert("RGB"), out_path)

def flat_icon(text, out_path, px=1024, r_frac=FLAT_RFRAC, hard_rfrac=0.5):
    """Flat square icon (iOS AppIcon, web favicon/PWA) — slate wordmark on near-white, no mask."""
    _save(render(text, px, SLATE, r_frac=r_frac, bg=BG, hard_rfrac=hard_rfrac).convert("RGB"), out_path)

# --- Notification small icon: solid disc with the app's initial knocked out -------
import re as _re
from fontTools.ttLib import TTFont as _TTFont
from fontTools.pens.svgPathPen import SVGPathPen as _SVGPathPen

def _glyph_cubic_segments(letter, font=FONT):
    """The letter's outline as absolute M/L/C/Z segments (Q converted to C), font units y-up."""
    f = _TTFont(font); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    pen = _SVGPathPen(gs); gs[cmap[ord(letter)]].draw(pen)
    toks = _re.findall(r"[MLHVCQZ]|-?\d*\.?\d+(?:e-?\d+)?", pen.getCommands())
    i = 0; px = py = sx = sy = 0.0; segs = []
    while i < len(toks):
        c = toks[i]
        if c == "M": px, py = float(toks[i+1]), float(toks[i+2]); sx, sy = px, py; segs.append(('M', px, py)); i += 3
        elif c == "L": px, py = float(toks[i+1]), float(toks[i+2]); segs.append(('L', px, py)); i += 3
        elif c == "H": px = float(toks[i+1]); segs.append(('L', px, py)); i += 2
        elif c == "V": py = float(toks[i+1]); segs.append(('L', px, py)); i += 2
        elif c == "C": x1,y1,x2,y2,x3,y3 = map(float, toks[i+1:i+7]); segs.append(('C',x1,y1,x2,y2,x3,y3)); px,py=x3,y3; i += 7
        elif c == "Q":
            x1,y1,x2,y2 = map(float, toks[i+1:i+5])
            segs.append(('C', px+2/3*(x1-px), py+2/3*(y1-py), x2+2/3*(x1-x2), y2+2/3*(y1-y2), x2, y2)); px,py=x2,y2; i += 5
        elif c == "Z": segs.append(('Z',)); px, py = sx, sy; i += 1
        else: i += 1
    return segs

def notification_icon(letter, out_path, target_h=9.0, radius=11.0, ystretch=YSTRETCH):
    """Write ic_notification.xml: a 24x24 white disc with `letter` (Baloo Chettan 2) knocked
    out (one evenOdd path), vertically stretched (ystretch) to match the launcher wordmark's
    letterform. White-on-transparent; Android tints it. Matches the family standard."""
    segs = _glyph_cubic_segments(letter)
    xs = []; ys = []
    for s in segs:
        if s[0] in ('M', 'L'): xs += [s[1]]; ys += [s[2]]
        elif s[0] == 'C': xs += [s[1], s[3], s[5]]; ys += [s[2], s[4], s[6]]
    mnx, mxx, mny, mxy = min(xs), max(xs), min(ys), max(ys)
    CX = CY = 12.0; sc = target_h / (mxy - mny); gcx = (mnx+mxx)/2; gcy = (mny+mxy)/2
    # height stays target_h; x is narrowed by ystretch → same taller/narrower letterform as the wordmark
    def tx(x, y): return (CX + (x-gcx)*(sc/ystretch), CY - (y-gcy)*sc)   # center + y-flip + vertical stretch
    fm = lambda v: f"{v:.3f}"; out = []
    for s in segs:
        if s[0] == 'M': X, Y = tx(s[1], s[2]); out.append(f"M {fm(X)},{fm(Y)}")
        elif s[0] == 'L': X, Y = tx(s[1], s[2]); out.append(f"L {fm(X)},{fm(Y)}")
        elif s[0] == 'C':
            a = tx(s[1], s[2]); b = tx(s[3], s[4]); c = tx(s[5], s[6])
            out.append(f"C {fm(a[0])},{fm(a[1])} {fm(b[0])},{fm(b[1])} {fm(c[0])},{fm(c[1])}")
        elif s[0] == 'Z': out.append("Z")
    glyph = " ".join(out)
    disc = f"M{CX-radius},{CY} a{radius},{radius} 0 1,0 {2*radius},0 a{radius},{radius} 0 1,0 {-2*radius},0 Z"
    xml = ('<!-- Notification status-bar icon (Hora-family standard): a SOLID disc with the\n'
           "     app's Malayalam initial in Baloo Chettan 2 knocked out (one evenOdd path).\n"
           '     White-on-transparent; Android tints it. Generated by gen_launcher_icon.notification_icon. -->\n'
           '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
           '    android:width="24dp" android:height="24dp"\n'
           '    android:viewportWidth="24" android:viewportHeight="24">\n'
           '    <path android:fillColor="#FFFFFF" android:fillType="evenOdd"\n'
           f'        android:pathData="{disc} {glyph}" />\n</vector>\n')
    _save_text(out_path, xml)

def _save_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh: fh.write(text)

# Per-app configs (the family standard, parameterised). Varisankya's agent fills in
# its own paths and runs `python gen_launcher_icon.py varisankya` to adopt the standard.
APPS = {
    "pathivu": dict(
        text="പതി", letter="പ", ios_dir="Pathivu",
        repo=r"C:\Users\Aarsh\Source\pathivu\pathivu",
    ),
    "varisankya": dict(
        text="വരി", letter="വ", ios_dir="Varisankya",
        repo=r"C:\Users\Aarsh\Source\varisankya\varisankya",
    ),
    "muthal": dict(
        text="മുത", letter="മ", ios_dir="Muthal",
        repo=r"C:\Users\Aarsh\Source\muthal\muthal",
    ),
}

def generate_all(cfg):
    repo = cfg["repo"]; res = os.path.join(repo, "android", "app", "src", "main", "res")
    generate(cfg["text"], res)                                                    # Android launcher (all densities + monochrome + legacy/round)
    notification_icon(cfg["letter"], os.path.join(res, "drawable", "ic_notification.xml"))  # Android notification
    flat_icon(cfg["text"], os.path.join(repo, "ios", cfg["ios_dir"], "Resources",
                                        "Assets.xcassets", "AppIcon.appiconset", "AppIcon-1024.png"))  # iOS
    web = os.path.join(repo, "web")
    flat_icon(cfg["text"], os.path.join(web, "app", "icon.png"), 192)
    flat_icon(cfg["text"], os.path.join(web, "public", "apple-touch-icon.png"), 180)
    flat_icon(cfg["text"], os.path.join(web, "public", "icon-192.png"), 192)
    flat_icon(cfg["text"], os.path.join(web, "public", "icon-512.png"), 512)
    flat_icon(cfg["text"], os.path.join(web, "public", "icon-maskable-512.png"), 512,
              r_frac=MASK_RFRAC, hard_rfrac=MASK_SAFE_HARD)
    play_icon(cfg["text"], os.path.join(repo, "android", "play_icon_512.png"))

if __name__ == "__main__":
    import sys
    app = sys.argv[1] if len(sys.argv) > 1 else "pathivu"
    generate_all(APPS[app])
    print(f"generated all {app} icons (launcher + notification + iOS + web + Play)")
