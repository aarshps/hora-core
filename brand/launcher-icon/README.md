# Launcher / app icon — Hora-family standard (Baloo Chettan 2 wordmark)

Every Hora app's icon is its short name as a Malayalam **wordmark** — Pathivu **പതി**,
Varisankya **വരി**, Muthal **മുത** — set in **Baloo Chettan 2** (the rounded family font,
OFL), slate `#445353` on near-white `#FCFCFC`, laid out under the **v3 six-line geometry**
below so every app's icon is identically sized, positioned, and wide.

This is the **single source of truth + generator** for ALL icons across the family and
all platforms. One engine, one look.

## The standard (v3 geometry locked 2026-07-03, signed off by the owner)
- **Font:** Baloo Chettan 2, weight **700** (`fonts/BalooChettan2-700.ttf`, OFL — see `fonts/OFL.txt`).
- **Wordmark:** the app's short Malayalam name, shaped with harfbuzz (correct ligatures/positioning).
- **Proportions:** **+45% vertical stretch** (`YSTRETCH=1.45`), plus the per-app **horizontal
  stretch** required by the width rule below (Pathivu 1.0 — the reference; Varisankya 1.116;
  Muthal 1.066).
- **Geometry — the six-line rule (locked 2026-07-03):** four guides are **family invariants**
  (identical in every app, on every surface); two are per-app:
  1. **Fixed letter size** — the *base-letter band* (the ink band of a plain base consonant,
     പ/മ/വ/ത — they share one band in this font) renders exactly `BAND_FRAC × canvas` high.
  2. **Fixed position** — the band's centre sits on the canvas centre, so **band top** and
     **baseline** land at the same y in every icon.
  3. **Fixed width** — ink width = `WIDTH_RATIO (2.4741) × band height`; each wordmark is
     x-stretched to it and centred, so **ink left/right** land at the same x in every icon.
     (Letter-spacing was evaluated and rejected: with one letter-gap per wordmark it triples
     Varisankya's gap. X-stretch is the same anisotropic family move as `YSTRETCH`.)
  4. **Natural extenders** — vowel signs (ി ascender / ു descender) extend freely beyond the
     band; the ascender-top and descender-bottom lines are the two per-app guides.
  5. **Safe-fit** — the FULL ink must fit each surface's safe circle (adaptive `0.305`,
     maskable `0.40`). The family constants carry verified headroom; the engine warns loudly
     if a wordmark would ever trip the clamp (that means: revisit the constants family-wide,
     never ship an off-standard icon).

  ![six-line rule](icon-geometry-standard.png)

  Per-surface band sizes (`BAND_FRAC`, calibrated so Pathivu's shipped icons are unchanged
  from the previous circle rule): Play 512 `0.2867` · flat squares (iOS AppIcon, web
  favicon/PWA "any") `0.2098` · Android legacy+round launcher `0.2398` · adaptive
  foreground + monochrome `0.1720` · maskable web `0.1678`.
- **Colours:** slate `#445353`, background `#FCFCFC`.
- **Rendering:** **FreeType** (the font's own nonzero rasteriser) — so self-intersecting Malayalam
  strokes (e.g. ത) fill correctly with **no holes**, and edges are crisp.

## The engine — `gen_launcher_icon.py`
Generates **every** icon for an app from the one spec:
- Android launcher: `mipmap-*/ic_launcher_foreground.png` (all densities), `drawable-nodpi/ic_launcher_monochrome.png`, legacy `ic_launcher.png` + `ic_launcher_round.png`.
- Android notification: `drawable/ic_notification.xml` (a solid disc with the app's initial in Baloo Chettan 2 knocked out — `notification_icon('പ', …)`).
- iOS: `AppIcon-1024.png`. Web: `app/icon.png`, `public/{apple-touch-icon,icon-192,icon-512,icon-maskable-512}.png`. Play: `play_icon_512.png` (written outside `res/`; upload to the listing manually).

Run (Pathivu is the reference consumer):
```
pip install uharfbuzz freetype-py fonttools brotli numpy pillow
python gen_launcher_icon.py pathivu      # or:  python gen_launcher_icon.py varisankya
```
Per-app config (text, initial letter, repo path, iOS module dir) is the `APPS` dict in the script.
**Varisankya's agent** adds/uses its config and runs `… varisankya` to adopt the standard — same algorithm, same look.

## Notification icon — same standard, same engine
The notification-shade icon is **a solid white disc with the app's Malayalam initial
knocked out as a hollow**, drawn as a single `evenOdd` vector path (disc *minus* glyph)
in `drawable/ic_notification.xml`. The art is white-on-transparent — Android tints the
small icon itself (white in the status bar, themed in the shade), so no colour decision
belongs in the file. The engine emits it via `notification_icon(<initial>, …)` from the
**same Baloo Chettan 2** glyph as the launcher, **vertically stretched the same 1.45×**
(`YSTRETCH`) so the status-bar initial and the wordmark share one letterform.

This is a firm family standard: **do not** revert to a framed, outlined, or
stroked-glyph treatment. The glyph is a *filled silhouette knocked out of the disc*
(negative space), not a stroked outline. (An earlier family icon used a rounded-square
outline frame around a stroked letter — that is superseded.)

## Reusing for a new sibling app
Add an entry to `APPS` (its Malayalam short name + initial + repo + iOS dir) and run it.
Nothing else to tune — the standard (font, weight, stretch, geometry, colours, rasteriser)
is fixed here. The engine computes the new wordmark's x-stretch automatically and **raises**
if it falls outside `[0.98, 1.20]` — that means the wordmark is too narrow/wide for the
family width and revisiting `WIDTH_RATIO` is a deliberate family decision (all apps regen
together), never a silent per-app tweak.

## Legacy
`varisankya-vari-reference.xml/.png` are the **old** hand-authored "വരി" vector (the prior gold
standard) kept for history. The previous per-app raster pipeline (`_tools/match_icon.py` +
`gen_icons.py`) and the earlier standalone notification-icon generator are **superseded** by
this single engine.
