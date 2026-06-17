# Notification status-bar icon — Hora-family standard

Every Hora Android app uses the same notification-shade icon language: a
**solid round (filled white disc) with the app's Malayalam initial knocked
out as a hollow** (negative space), drawn as a single `evenOdd` vector path
(disc *minus* glyph). The art is plain white-on-transparent — Android tints
the small icon itself (white in the status bar, themed in the shade), so no
color decisions belong in this file.

**Do not** revert to a framed, outlined, or stroked-glyph treatment.
Solid-disc-with-hollow-initial is the standard across the family.

> **Migrating from the older framed treatment.** An earlier version of this
> icon used a rounded-square *outline frame* around a *stroked* (outlined)
> letter. That is superseded — ratified family-wide on the Varisankya icon.
> If an app still ships the framed/stroked version, regenerate it with this
> tool. Note the key difference: the glyph here is a **filled silhouette
> knocked out of the disc** (negative space), **not** a stroked outline — so
> build the initial's solid silhouette for `GLYPH_PATH`; don't shrink an
> existing stroked path.

## Per app

Each app's initial is different (Varisankya = "വ", Pathivu = its own letter,
…), so each app keeps its **own** generated `ic_notification.xml` — there is
no runtime-shared drawable. What's shared is the *construction*:

1. Copy [`gen_notification_icon.py`](gen_notification_icon.py) into the app's
   `android/tools/`.
2. Replace `GLYPH_PATH` with that app's Malayalam initial silhouette,
   absolute `M/L/C/Z` commands, centred on `(12,12)` in a 24×24 viewport.
3. `python gen_notification_icon.py preview` to compare glyph scales (status
   bar / notification-shade card / 36px contexts side by side).
4. `python gen_notification_icon.py emit <scale>` to write the final
   `ic_notification.xml`. Varisankya uses scale `0.85` — bold yet legible at
   24dp. Pick whatever scale reads cleanly for the new glyph; it won't
   necessarily be the same number.

## Consumption mechanism

This is a **dev-time generator**, not a runtime dependency — there's no
Kotlin/Swift/TS code-sharing involved (see [`docs/conventions.md`](../../docs/conventions.md)
§ Cross-language code sharing). Each app copies the script locally and
customizes `GLYPH_PATH`. `hora-core` is the canonical source for the
*standard and the generator*; if the generation logic changes, update it
here first and re-copy into each app.
