---
name: hora-launcher-icon
description: Generate ALL Hora-family app icons (Android launcher + notification, iOS, web, Play) from the shared Baloo Chettan 2 wordmark engine in hora-core. Use when creating or refining any Hora app's icons.
---

# Hora app icons — one engine, Baloo Chettan 2 wordmark

**As of 2026-06 there IS a shared engine** — use it, don't hand-tune per app. The family icon is the
app's short Malayalam name (Pathivu **പതി**, Varisankya **വരി**, Muthal **മുത**) set in **Baloo Chettan 2**
(700, +45% vertical stretch), slate **#445353** on **#FCFCFC**, centered.
**Sizing (locked 2026-07 — the "max-in-circle" rule):** the wordmark is scaled so its circumscribing
circle (centred on the canvas) is the **largest circle that fits the icon's usable area** — max size
in that circle. `r_frac` = circle radius / canvas: `FULL_RFRAC=0.5` (unmasked/circular: Play, iOS, web
favicon/PWA-any, legacy+round launcher), `FG_RFRAC=0.305` (adaptive foreground + monochrome safe
circle), `MASK_RFRAC=0.40` (maskable web safe circle). Canonical generator + font + full spec:
**[`brand/launcher-icon/`](../../../brand/launcher-icon/README.md)** → `gen_launcher_icon.py`.

```
pip install uharfbuzz freetype-py fonttools brotli numpy pillow
python gen_launcher_icon.py <app>      # writes launcher (all densities) + monochrome + legacy/round
                                       # + notification (ic_notification) + iOS + web + Play 512
```

It uses harfbuzz (shaping) + **FreeType** (the font's own nonzero rasteriser — correct fill, no holes
in self-intersecting glyphs like ത). Add a new sibling by adding an `APPS` entry (Malayalam name +
initial + repo path + iOS dir). **Always get explicit user sign-off before shipping — this icon is
highly scrutinised.**

The legacy material below (matching the old hand-drawn Varisankya reference with per-app font tuning,
`varisankya-vari-reference.xml`) is **superseded** by the engine; kept only as history.

## Method (what actually works — learned over several iterations on prior apps)
1. **Graft any shared subglyph exactly**, when the app's name shares a letterform with the
   reference (e.g. a vowel sign). Extract that subpath verbatim from the reference vector XML
   (`brand/launcher-icon/varisankya-vari-reference.xml`; parse the path commands; identify the
   shared subpath) rather than redrawing it, so it stays
   pixel-identical.
2. **Render each letter SEPARATELY** rather than as a shaped string — engines like Pillow lack
   proper complex-script shaping, so render via a shaping-aware path (e.g. GDI+/`System.Drawing`
   on Windows) and control inter-letter gap manually. Pick a face deliberately and get user
   sign-off on the face choice early — don't chase a stroke-width match by swapping fonts later;
   match weight by trimming the chosen face instead. The family has so far standardized on
   **Baloo 2 Bold** (rounded, bold; a monoline face like Manjari was tried and rejected on sight) —
   start there and confirm, rather than re-deriving the face per app.
3. **Match the reference's stroke weight by uniform trim**, measured against the reference's own
   stem width at a fixed x-height. Apply uniform erosion (shrinks bowls too, not just stems)
   rather than directional erosion, which leaves bowls heavy and never reads as thinner.
4. **Match height first, then fit the bounding circle.** Render at the reference's x-height,
   compress width to the reference's aspect ratio so it fits the same centered circle, then
   restore stroke weight lost to compression via *horizontal-only* dilation (so the compression
   doesn't re-thin the glyph).
5. **Assemble with the inter-letter gap added after stroke-restore**, not before (adding it before
   compression collapses it into a collision). Keep any grafted shared subglyph (step 1) out of
   any width compression — compressing the whole word also shrinks the shared part, which should
   stay pixel-identical to the reference.
6. **Contour-smooth the composed master before downsampling.** The horizontal-only
   weight-restore (step 4) leaves flat rectangular ledges — "tabs/spikes" — on the vertical stems
   that don't follow the curve and survive the per-density downsample as pixel-level spikes.
   Gaussian-blur the hi-res master, then re-threshold at 50% alpha: this dissolves the tabs (and
   any narrow notches) while leaving straight stem edges exactly in place, so stroke weight is
   preserved (verify a stem stays its target px width after). Tune the blur radius on a 5× zoom
   before/after (≈10 master-res px worked for one app).
7. **Generate the full mipmap set** (`ic_launcher`, `ic_launcher_foreground`, `ic_launcher_round`,
   plus a monochrome `drawable-nodpi` for the adaptive icon) sized by the reference's own
   bounding-circle fraction, so the new icon visually matches the reference's fill/padding inside
   the adaptive mask.

## Gotchas
- Any dilation/erosion step must grow into a padded canvas first, or it clips the edge letters.
- Add the inter-letter gap on separate glyphs, after compression — not before.
- Keep grafted shared subglyphs out of width-compression so they don't shrink.
- Horizontal-only weight-restore leaves jagged stem tabs; contour-smooth the master (blur +
  re-threshold at 50%) before downsampling (step 6), or they survive as pixel spikes at small sizes.
- The **Play Store listing icon is a separate asset**, sized/measured differently — see
  `hora-play-store`.

## Verify before shipping
Render a side-by-side comparison against the reference icon and get **explicit user sign-off**
before generating final assets. Then ship via `hora-app-release`.
