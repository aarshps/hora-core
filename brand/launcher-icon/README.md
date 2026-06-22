# Launcher / app icon — Hora-family standard (Baloo Chettan 2 wordmark)

Every Hora app's icon is its short name as a Malayalam **wordmark** — Pathivu **പതി**,
Varisankya **വരി** — set in **Baloo Chettan 2** (the rounded family font, OFL), slate
`#445353` on near-white `#FCFCFC`, centered, sized to a fixed bounding circle.

This is the **single source of truth + generator** for ALL icons across the family and
all platforms. One engine, one look.

## The standard (locked 2026-06, signed off by the owner)
- **Font:** Baloo Chettan 2, weight **700** (`fonts/BalooChettan2-700.ttf`, OFL — see `fonts/OFL.txt`).
- **Wordmark:** the app's short Malayalam name, shaped with harfbuzz (correct ligatures/positioning).
- **Proportions:** **+45% vertical stretch** (`YSTRETCH=1.45`), **no horizontal squeeze**.
- **Size/position:** centered; bounding-circle radius = **`R_FRAC=0.2435`** of the canvas (the size
  the icon has always used). Flat icons (iOS/web/Play) use a fuller `R_FRAC≈0.30` (0.24 for maskable).
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

## Reusing for a new sibling app
Add an entry to `APPS` (its Malayalam short name + initial + repo + iOS dir) and run it. Nothing else to tune — the standard (font, weight, stretch, size, colours, rasteriser) is fixed here.

## Legacy
`varisankya-vari-reference.xml/.png` are the **old** hand-authored "വരി" vector (the prior gold
standard) kept for history. The previous per-app raster pipeline (`_tools/match_icon.py` +
`gen_icons.py`) and the separate `brand/notification-icon/` flow are **superseded** by this engine.
