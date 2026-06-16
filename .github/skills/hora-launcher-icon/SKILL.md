---
name: hora-launcher-icon
description: Generate a "Hora"-family Android launcher icon — the app's short name drawn to match the family's established hand-drawn icon style pixel-for-pixel. Use when creating or refining the launcher/adaptive icon for any Hora app.
---

# Hora launcher icon (wordmark, matched to the family reference)

Hora apps share one icon language: the app's short name in slate **#445353** on **#FCFCFC**,
drawn to match the established family reference icon (Varisankya's **വരി**, a hand-authored
vector in its `ic_launcher_monochrome.xml` — NOT a font). Never expect an installed font to match
the reference outright; compose the glyph programmatically against the reference's actual
measurements.

There is no shared, importable script library for this — each app's icon needs its own iterative
tuning pass (font, weight-trim, compression) against the reference's measured metrics, followed
by **explicit user sign-off before shipping** (this icon is highly scrutinised). Treat the method
below as the reusable asset; rebuild the generator scripts per-app from it rather than assuming a
prior app's tuned script transfers as-is.

## Method (what actually works — learned over several iterations on prior apps)
1. **Graft any shared subglyph exactly**, when the app's name shares a letterform with the
   reference (e.g. a vowel sign). Extract that subpath verbatim from the reference's vector XML
   (parse the path commands; identify the shared subpath) rather than redrawing it, so it stays
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
6. **Generate the full mipmap set** (`ic_launcher`, `ic_launcher_foreground`, `ic_launcher_round`,
   plus a monochrome `drawable-nodpi` for the adaptive icon) sized by the reference's own
   bounding-circle fraction, so the new icon visually matches the reference's fill/padding inside
   the adaptive mask.

## Gotchas
- Any dilation/erosion step must grow into a padded canvas first, or it clips the edge letters.
- Add the inter-letter gap on separate glyphs, after compression — not before.
- Keep grafted shared subglyphs out of width-compression so they don't shrink.
- The **Play Store listing icon is a separate asset**, sized/measured differently — see
  `hora-play-store`.

## Verify before shipping
Render a side-by-side comparison against the reference icon and get **explicit user sign-off**
before generating final assets. Then ship via `hora-app-release`.
