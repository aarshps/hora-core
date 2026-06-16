---
name: skeleton-loading-standards
description: Skeleton-placeholder loading standards for Hora-family Android apps — structural parity, M3 surface tonality, and a reveal transition into real content.
---

# Skeleton loading standards

Data-driven screens show a skeleton that mimics the final content structure, then reveal
real data — an "ultra smooth" load with no blank screen or spinner gap.

## Principles
1. **Structural parity.** Skeleton blocks match the real components' proportions, margins,
   and shapes — the same layout, greyed out.
2. **Surface tonality.** Use `colorSurfaceContainerHigh` / `colorSurfaceContainerHighest`
   for the skeleton blocks — distinct but flat, on-brand M3.
3. **Implicit shimmer.** Skeletons don't need an aggressive shimmer animation; the
   perceived motion comes from the transition into real data.

## Implementation
- Build a composite skeleton layout that `include`s the per-item skeletons (e.g. a hero
  skeleton plus a few row skeletons), shown while loading.
- On data ready, hide the skeleton and reveal the real content with a reveal animation,
  optionally bridged by a light haptic.

## Reveal parameters
- Duration ~400–500ms.
- Interpolator: **emphasized** (M3 standard).
- Optional: a click / segment-tick haptic on reveal (guarded — see `m3e-haptic-standards`).

## Checklist
- [ ] Skeleton mirrors the real layout's structure, margins, and shapes.
- [ ] Blocks use a high surface-container tone, not arbitrary greys.
- [ ] Reveal is ~400–500ms on the emphasized curve.
