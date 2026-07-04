#!/usr/bin/env python3
"""
Hora-family brand-mark engine (FINAL) — the single source for every icon and every
wide-card brand asset the family ships, on every platform and every surface.

The family mark is a Malayalam wordmark (Pathivu "പതി", Varisankya "വരി", Muthal "മുത")
set in **Baloo Chettan 2** (rounded, OFL) in slate on near-white, laid out under the
**v3 six-line geometry standard** (see the constants block): in every icon, on every
surface, the base letters render at the same fixed size, centred, and the ink at the
same fixed width. Rendering uses harfbuzz (shaping) + FreeType (the font's own nonzero
rasterizer — no fill-rule holes), so edges are crisp and the ത/പ counters are correct.

This is a STRICT, exhaustive family standard, not a hedged reference — it covers every
icon surface (Android launcher/adaptive/monochrome/legacy/round, the notification disc,
iOS AppIcon, web favicon/PWA/maskable) AND every wide "glyph + name + tagline" brand
card (Play Store listing icon + feature graphic, the Next.js Open Graph/Twitter social
image, the GitHub repository social-preview card) through the ONE `_wide_card()`
composer. There is no surface where a Hora app's brand mark is hand-authored, ad-hoc,
or a platform default (a generic favicon, GitHub's auto-generated social card, no
social-share image at all) — see `conventions.md` -> "Brand mark standard" for the
full enumerated list and the MUST-language rule.

One algorithm, every app, every surface: pass a different `text` (and paths). Run from
anywhere. Deps: uharfbuzz, freetype-py, fontTools (woff2->ttf), numpy, Pillow.
"""
import os, sys, math
import numpy as np
import uharfbuzz as hb
import freetype
from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

# ---- Family standard (locked with Aarsh, 2026-06) --------------------------
FONT      = os.path.join(FONTS, "BalooChettan2-700.ttf")  # Baloo Chettan 2, weight 700
SLATE     = (0x44, 0x53, 0x53)
BG        = (0xFC, 0xFC, 0xFC)
YSTRETCH  = 1.45     # vertical stretch ("taller")
EM        = 2000     # FreeType em pixels (hi-res master for crisp downsamples)

# ---- Icon geometry standard v3 (locked with Aarsh, 2026-07-03) -----------------------
# THE SIX-LINE RULE. In every Hora icon, on every surface, these four guides are
# FAMILY INVARIANTS (identical position in every app):
#   band top / baseline        — the base-letter band (see "band rule" below)
#   ink left / ink right      — the wordmark's horizontal extent
# and these two are per-app, bounded by the safe-fit check:
#   ascender top (ി/ീ)         descender bottom (ു)
#
#   R1 FIXED LETTER SIZE — the band renders BAND_FRAC*canvas high on each surface.
#                          (Replaces the earlier circle-diagonal rule, which coupled
#                          letter size to wordmark width: an 8.9% size spread.)
#   R2 FIXED POSITION    — the band's vertical centre sits Y_SHIFT_FRAC*canvas BELOW the
#                          canvas centre (locked 2026-07-04, revised same day to 2%).
#                          History: dead-centre (0%) read as too high on first review;
#                          4% was tried next but over-corrected — with one SHARED line
#                          across apps, Muthal (descender-only, no ascender) sank
#                          visibly, while Pathivu/Varisankya (ascender-only) looked
#                          right. Principled family-fair analysis (centroid-centering
#                          each app, then averaging/minimax across all three) converges
#                          to ~0-0.3%, confirming a uniform shift can't optically serve
#                          an ascender-heavy and a descender-heavy app at once — any
#                          uniform value is a deliberate compromise, not a computed
#                          optimum. Final call after side-by-side review: 2% down —
#                          perceptibly off dead-centre without Muthal sinking, with a
#                          worst-case 3.43pp margin under the tightest safe-fit clamp
#                          (Muthal on the adaptive-foreground surface; FG allows up to
#                          7.16% before tripping; PLAY/LAUNCHER/FLAT/MASK allow far more).
#   R3 FIXED WIDTH       — ink width = WIDTH_RATIO * band height; each wordmark is
#                          x-stretched to it. Same anisotropic-scaling family move as
#                          YSTRETCH, on the other axis. Tracking was evaluated and
#                          rejected (Varisankya's single letter-gap would triple).
#   R4 NATURAL EXTENDERS — vowel signs extend freely beyond the band (treatment A;
#                          compression variants were reviewed and declined).
#   R5 SAFE-FIT          — the FULL ink must fit the surface's safe circle (adaptive
#                          0.305, maskable 0.40). The family constants carry headroom
#                          for all current apps; the clamp in render() must never
#                          bind — if it does, revisit the constants family-wide.
#
# Calibration: BAND_FRAC preserves Pathivu's shipped rendering under the previous rule
# (band_frac = 2*r_frac*band_h/hypot(w_pathivu, band_h); w_pathivu/band_h = 2.4741), and
# WIDTH_RATIO is Pathivu's natural width ratio — so Pathivu is the do-nothing reference
# (x-stretch 1.0) and siblings stretch to it (Varisankya 1.116, Muthal 1.066).
# Per-surface sizes (why they differ): Play is re-cropped + shadow-framed by Play's own
# chrome; the adaptive foreground / maskable icons answer to their safe circles; the
# flat squares + full-bleed launcher carry the established family margins.
PLAY_BAND_FRAC     = 0.2867   # Play Store 512 listing icon
FLAT_BAND_FRAC     = 0.2098   # flat squares: iOS AppIcon + web favicon / PWA "any"
LAUNCHER_BAND_FRAC = 0.2398   # Android legacy + round launcher (slate-on-BG square)
FG_BAND_FRAC       = 0.1720   # Android adaptive foreground + monochrome
MASK_BAND_FRAC     = 0.1678   # maskable web icon
WIDTH_RATIO        = 2.4741   # family ink width / band height (R3)
Y_SHIFT_FRAC       = 0.02     # band centre offset below canvas centre, all surfaces (R2)
XS_MIN, XS_MAX     = 0.98, 1.20  # allowed per-app x-stretch; outside -> family decision
FG_SAFE_HARD   = 0.305   # adaptive-icon safe circle — full ink must never exceed this
MASK_SAFE_HARD = 0.40    # W3C maskable safe circle — full ink must never exceed this

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

def render(text, canvas_px, color, band_frac=FLAT_BAND_FRAC, bg=None, circle=False, ss=4, hard_rfrac=0.5):
    """Wordmark rendered under the v3 six-line geometry: the base-letter BAND renders
    band_frac*canvas high (R1) with its centre Y_SHIFT_FRAC*canvas below the canvas
    centre (R2); the ink is x-stretched to WIDTH_RATIO*band_h wide (R3) and centred;
    ascenders/descenders extend naturally beyond the band (R4). `hard_rfrac` is the R5
    safe-fit clamp — under the family constants it must never bind; if a future
    wordmark trips it the engine warns loudly (the icon would fall off-standard) and
    scales down to fit, band kept at its shifted centre. Optional bg / circle mask as
    before. The safe-fit clamp is measured from the CANVAS centre (not the shifted
    band centre), since the safe circle itself is canvas-centred."""
    S = canvas_px * ss
    m, base = wordmark_mask_with_baseline(text); w, h = m.size
    band_h, band_top_rel = _band()
    # R3 fixed ink width — x-stretch to the family ratio (Pathivu = 1.0).
    xs = WIDTH_RATIO * band_h / w
    if not (XS_MIN <= xs <= XS_MAX):
        raise ValueError(
            f"wordmark '{text}' needs x-stretch {xs:.3f}, outside [{XS_MIN}, {XS_MAX}] — "
            "revisiting WIDTH_RATIO is a deliberate family decision (see the README)")
    if abs(xs - 1.0) > 1e-3:
        m = m.resize((max(1, round(w * xs)), h), Image.LANCZOS); w = m.width
    band_center = base + band_top_rel + band_h / 2.0        # row of band centre in mask
    s = band_frac * S / band_h                              # R1 fixed letter size
    cy = S / 2.0 + Y_SHIFT_FRAC * S                          # R2 shifted band centre

    def _corner_dist(scale):
        """Farthest ink corner's distance from the CANVAS centre (S/2,S/2) — the safe
        circle is canvas-centred, not shifted-band-centred, so this must be measured
        from the true centre even though the ink itself sits lower."""
        top_y = cy - band_center * scale; bot_y = cy + (h - band_center) * scale
        dx = (w * scale) / 2.0
        return max(math.hypot(dx, abs(top_y - S / 2.0)), math.hypot(dx, abs(bot_y - S / 2.0)))

    # R5 safe-fit clamp on the FULL ink box. Fixed-point correction (the shift means
    # dmax isn't purely linear in s) — converges in a couple of steps; current family
    # constants never enter this branch (verified with margin for all 3 apps).
    dmax = _corner_dist(s)
    if dmax > hard_rfrac * S:
        print(f"WARNING: '{text}' trips the {hard_rfrac} safe-fit clamp — this icon is "
              "OFF-standard (smaller letters than its siblings); revisit the family "
              "constants instead of shipping it.", file=sys.stderr)
        for _ in range(4):
            s *= (hard_rfrac * S) / _corner_dist(s)
    tw = max(1, round(w * s)); th = max(1, round(h * s))
    m = m.resize((tw, th), Image.LANCZOS)
    alpha = Image.new("L", (S, S), 0)
    alpha.paste(m, ((S - tw) // 2, round(cy - band_center * s)))
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
        _save(render(text, px, SLATE, band_frac=FG_BAND_FRAC, hard_rfrac=FG_SAFE_HARD),
              os.path.join(res_dir, f"mipmap-{dpi}", "ic_launcher_foreground.png"))
    _save(render(text, 432, (0, 0, 0), band_frac=FG_BAND_FRAC, hard_rfrac=FG_SAFE_HARD),
          os.path.join(res_dir, "drawable-nodpi", "ic_launcher_monochrome.png"))
    for dpi, px in LG.items():
        _save(render(text, px, SLATE, band_frac=LAUNCHER_BAND_FRAC, bg=BG).convert("RGB"),
              os.path.join(res_dir, f"mipmap-{dpi}", "ic_launcher.png"))
        _save(render(text, px, SLATE, band_frac=LAUNCHER_BAND_FRAC, bg=BG, circle=True),
              os.path.join(res_dir, f"mipmap-{dpi}", "ic_launcher_round.png"))

def play_icon(text, out_path):
    """Play Store 512 listing icon (full-bleed square). Letters sized by PLAY_BAND_FRAC
    (smaller than full-bleed) so the mark doesn't read as cramped inside Play's own
    grid/detail chrome — the established family look. Write OUTSIDE res/ (not a build
    resource)."""
    _save(render(text, 512, SLATE, band_frac=PLAY_BAND_FRAC, bg=BG).convert("RGB"), out_path)

def flat_icon(text, out_path, px=1024, band_frac=FLAT_BAND_FRAC, hard_rfrac=0.5):
    """Flat square icon (iOS AppIcon, web favicon/PWA) — slate wordmark on near-white, no mask."""
    _save(render(text, px, SLATE, band_frac=band_frac, bg=BG, hard_rfrac=hard_rfrac).convert("RGB"), out_path)

# --- Play Store listing design language: feature graphic --------------------------
# Locked with Aarsh, 2026-07-04. Same brand primitives as the icons (Baloo wordmark,
# slate/BG, the band-rule render() incl. its Y-shift) plus Google Sans Flex at ROND=100
# for the Latin name + tagline (per the "Marketing & static-image typography" rule).
GSF_VARIABLE = os.path.join(HERE, "..", "..", "shared", "android", "res", "font",
                             "google_sans_flex_variable.ttf")
# Wide-card standard (locked 2026-07-04, extended 2026-07-04): ONE composer, reused at
# every "glyph + Latin name + tagline" surface the family needs — Play feature graphic,
# Next.js Open Graph / Twitter social image, GitHub repo social preview. Font sizes and
# margins below are calibrated at the Play feature graphic's 500px height and scale
# proportionally to whatever height the caller asks for, so every surface reads as the
# same design at a different aspect ratio, never a re-tuned one-off.
_CARD_REF_H = 500                    # the height the constants below were tuned at
_CARD_GLYPH_BAND_FRAC = 0.26         # tuned for the glyph area in this composition
_CARD_ACCENT_W = 34                  # right-edge slate accent bar, at _CARD_REF_H
_CARD_MARGIN = 40                    # left margin + glyph-to-text gap, at _CARD_REF_H
_CARD_NAME_PX = (84, 48)             # (start, floor) font size for the name, at _CARD_REF_H
_CARD_TAG_PX = (34, 20)              # (start, floor) font size for the tagline, at _CARD_REF_H
_CARD_GAP = 18                       # name-to-tagline vertical gap, at _CARD_REF_H

def _fit_font(draw, text, max_w, start_px, min_px, axes):
    """Largest font size <= start_px (never below min_px) whose rendered width of
    `text` fits max_w. Raises rather than silently overflowing/clipping — a tagline
    that doesn't fit even at the floor size needs shortening, not silent damage."""
    px = start_px
    while px > min_px:
        f = ImageFont.truetype(GSF_VARIABLE, px); f.set_variation_by_axes(axes(px))
        bbox = draw.textbbox((0, 0), text, font=f)
        if bbox[2] - bbox[0] <= max_w:
            return f, bbox
        px -= 2
    f = ImageFont.truetype(GSF_VARIABLE, min_px); f.set_variation_by_axes(axes(min_px))
    bbox = draw.textbbox((0, 0), text, font=f)
    if bbox[2] - bbox[0] > max_w:
        raise ValueError(f"'{text}' doesn't fit even at the {min_px}px floor "
                          f"({bbox[2] - bbox[0]}px needed vs {max_w}px available) — "
                          "shorten the tagline or widen the text column")
    return f, bbox

def _wide_card(text, name_en, tagline_en, out_path, w, h):
    """The family's one 'glyph + Latin name + tagline' wide-card composer: the
    Malayalam wordmark glyph (rendered by the same render() used for every icon, so
    it carries the family band rule + Y-shift verbatim) on the left, the Latin app
    name (bold) + one-line tagline (regular) — both Google Sans Flex at ROND=100,
    shrunk to fit the column so a long tagline never overflows or clips — to its
    right, and a slate accent bar on the right edge. `w`/`h` scale every metric
    proportionally from the reference tuning at `_CARD_REF_H`, so every surface built
    on this composer (Play feature graphic, Next.js OG image, GitHub social preview)
    is the same design, not a re-tuned one-off."""
    k = h / _CARD_REF_H
    margin = _CARD_MARGIN * k
    accent_w = _CARD_ACCENT_W * k
    gap = _CARD_GAP * k
    # Only the START size scales with canvas height — the FLOOR is an absolute
    # legibility limit, not a proportion, and narrower-aspect cards (OG 1.9:1,
    # GitHub 2.0:1 vs the feature graphic's 2.05:1) need the full shrink range to
    # fit longer taglines (Varisankya's is the longest in the family).
    name_start, name_floor = _CARD_NAME_PX[0] * k, _CARD_NAME_PX[1]
    tag_start, tag_floor = _CARD_TAG_PX[0] * k, _CARD_TAG_PX[1]

    img = Image.new("RGB", (w, h), BG)
    glyph_px = h
    glyph = render(text, glyph_px, SLATE, band_frac=_CARD_GLYPH_BAND_FRAC, bg=None)
    img.paste(glyph, (round(margin), 0), glyph)

    d = ImageDraw.Draw(img)
    text_x = margin + glyph_px + margin / 2.0
    max_text_w = w - accent_w - margin * 0.75 - text_x

    f_name, name_bbox = _fit_font(d, name_en, max_text_w, name_start, name_floor,
                                   lambda px: [max(48, min(96, px)), 100, 700, 0, 100, 0])
    f_tag, tag_bbox = _fit_font(d, tagline_en, max_text_w, tag_start, tag_floor,
                                 lambda px: [px, 100, 500, 0, 100, 0])

    block_h = (name_bbox[3] - name_bbox[1]) + gap + (tag_bbox[3] - tag_bbox[1])
    y0 = (h - block_h) / 2 - name_bbox[1]
    d.text((text_x, y0), name_en, font=f_name, fill=SLATE)
    y1 = y0 + name_bbox[3] + gap - tag_bbox[1]   # tag ink-top = name ink-bottom + gap
    d.text((text_x, y1), tagline_en, font=f_tag, fill=SLATE)

    d.rectangle([w - accent_w, 0, w, h], fill=SLATE)
    _save(img, out_path)

FEATURE_W, FEATURE_H = 1024, 500     # Play Store's fixed feature-graphic size
OG_W, OG_H = 1200, 630               # Next.js / Open Graph / Twitter card standard size
GITHUB_SOCIAL_W, GITHUB_SOCIAL_H = 1280, 640   # GitHub's recommended social-preview size

def feature_graphic(text, name_en, tagline_en, out_path):
    """Play Store feature graphic (1024x500) — see _wide_card()."""
    _wide_card(text, name_en, tagline_en, out_path, FEATURE_W, FEATURE_H)

def og_image(text, name_en, tagline_en, out_path):
    """Next.js Open Graph / Twitter social-share image (1200x630), written to
    web/app/opengraph-image.png (Next.js's special-file convention auto-injects the
    og:image/twitter:image meta tags — no code change needed in the app). Closes a
    real gap: none of the family's web apps had a social-share image before this;
    sharing a link showed no preview or a browser default. Same composer as the Play
    feature graphic — see _wide_card()."""
    _wide_card(text, name_en, tagline_en, out_path, OG_W, OG_H)

def github_social_preview(text, name_en, tagline_en, out_path):
    """GitHub repository social-preview card (1280x640, GitHub's recommended size).
    Closes a real gap: every family repo currently shows GitHub's generic
    auto-generated card (repo name + the owner's personal avatar photo + stats) with
    no brand mark at all. GitHub has no API for this — the generated PNG must be
    uploaded by hand: repo Settings -> General -> Social preview -> Edit -> upload
    image. Same composer as the Play feature graphic — see _wide_card()."""
    _wide_card(text, name_en, tagline_en, out_path, GITHUB_SOCIAL_W, GITHUB_SOCIAL_H)

def family_social_preview(out_path, w=GITHUB_SOCIAL_W, h=GITHUB_SOCIAL_H,
                           name_en="hora-core", tagline_en="Shared building blocks for the Hora family"):
    """The hora-core repo's OWN GitHub social-preview card: not one app's wordmark but
    all of them side by side (every entry currently in APPS, in dict order), since this
    repo is the shared foundation under all three, not a consumer app itself. Same
    right-column composition as _wide_card() (name bold / tagline regular / accent bar)
    but the left area is a row of every family wordmark glyph instead of one — so this
    card updates automatically the day a new sibling app is added to APPS."""
    k = h / _CARD_REF_H
    margin = _CARD_MARGIN * k
    accent_w = _CARD_ACCENT_W * k
    gap = _CARD_GAP * k
    glyph_row_h = h * 0.30   # 3 glyphs side by side need far less height each than 1 alone
    glyphs = [render(cfg["text"], round(glyph_row_h), SLATE,
                      band_frac=_CARD_GLYPH_BAND_FRAC, bg=None) for cfg in APPS.values()]
    glyph_gap = margin * 0.5
    row_w = sum(g.width for g in glyphs) + glyph_gap * (len(glyphs) - 1)

    img = Image.new("RGB", (w, h), BG)
    gx = round(margin)
    gy = round((h - glyph_row_h) / 2)
    for g in glyphs:
        img.paste(g, (gx, gy), g)
        gx += g.width + round(glyph_gap)

    d = ImageDraw.Draw(img)
    text_x = margin + row_w + margin
    max_text_w = w - accent_w - margin * 0.75 - text_x

    name_start, name_floor = _CARD_NAME_PX[0] * k, _CARD_NAME_PX[1]
    tag_start, tag_floor = _CARD_TAG_PX[0] * k, _CARD_TAG_PX[1]
    f_name, name_bbox = _fit_font(d, name_en, max_text_w, name_start, name_floor,
                                   lambda px: [max(48, min(96, px)), 100, 700, 0, 100, 0])
    f_tag, tag_bbox = _fit_font(d, tagline_en, max_text_w, tag_start, tag_floor,
                                 lambda px: [px, 100, 500, 0, 100, 0])

    block_h = (name_bbox[3] - name_bbox[1]) + gap + (tag_bbox[3] - tag_bbox[1])
    y0 = (h - block_h) / 2 - name_bbox[1]
    d.text((text_x, y0), name_en, font=f_name, fill=SLATE)
    y1 = y0 + name_bbox[3] + gap - tag_bbox[1]
    d.text((text_x, y1), tagline_en, font=f_tag, fill=SLATE)

    d.rectangle([w - accent_w, 0, w, h], fill=SLATE)
    _save(img, out_path)

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
        name_en="Pathivu", tagline_en="Habit tracker",
    ),
    "varisankya": dict(
        text="വരി", letter="വ", ios_dir="Varisankya",
        repo=r"C:\Users\Aarsh\Source\varisankya\varisankya",
        name_en="Varisankya", tagline_en="Subscription & recurring-payment tracker",
    ),
    "muthal": dict(
        text="മുത", letter="മ", ios_dir="Muthal",
        repo=r"C:\Users\Aarsh\Source\muthal\muthal",
        name_en="Muthal", tagline_en="Income & expense ledger for institutions",
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
              band_frac=MASK_BAND_FRAC, hard_rfrac=MASK_SAFE_HARD)
    play_icon(cfg["text"], os.path.join(repo, "android", "play_icon_512.png"))
    feature_graphic(cfg["text"], cfg["name_en"], cfg["tagline_en"],
                     os.path.join(repo, "android", "play_feature_graphic.png"))  # Play Store listing
    og_image(cfg["text"], cfg["name_en"], cfg["tagline_en"],
             os.path.join(web, "app", "opengraph-image.png"))  # Next.js OG/Twitter card
    github_social_preview(cfg["text"], cfg["name_en"], cfg["tagline_en"],
                           os.path.join(repo, "github_social_preview.png"))  # manual upload, see docstring

if __name__ == "__main__":
    import sys
    app = sys.argv[1] if len(sys.argv) > 1 else "pathivu"
    generate_all(APPS[app])
    print(f"generated all {app} icons (launcher + notification + iOS + web + Play + "
          "OG image + GitHub social preview) -- upload github_social_preview.png by "
          "hand: repo Settings -> General -> Social preview")
