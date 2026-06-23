---
name: shared-android-source
description: Consume the Hora-family shared Android source (ChipHelper, ThemeHelper, AnimationHelper, design tokens) from hora-core/shared/android via sync_shared_android.sh — don't reimplement or hand-edit the generated copies.
---

# Shared Android source

hora-core is not just docs — `shared/android/` holds the **canonical Android source** every
Hora app uses verbatim. Apps consume it by copying it in with a tiny per-app sync script
(same "generated copies from hora-core" model as `.github/skills/`). There is no published
artifact.

## What lives there (see `shared/android/README.md` for the table)
- Design tokens: `res/values/dimens.xml`, `res/values/type.xml` (`TextAppearance.App.*`),
  `res/values/colors.xml` (the `mono_*` monochrome palette), `res/values/ids.xml`,
  `res/values/attrs.xml` (empty placeholder today).
- Widget & shape styles: `res/values/styles_shared.xml` (the byte-identical
  `Widget.App.*` / `ShapeAppearance.App.*` / `App.*` layer; app-specific theme config +
  divergent styles stay in each app's own `themes.xml`).
- Chip color selectors: `res/color/chip_{background,text,stroke}_color.xml` (+ `chip_stroke_app`,
  `outline_stroke_app`).
- Motion: `res/anim/slide_{in,out}_{left,right}.xml` (M3 nav transitions).
- Kotlin: `util/ChipHelper.kt`, `util/ThemeHelper.kt`, `util/AnimationHelper.kt`,
  `util/TimeProvider.kt` (injectable clock), and the top-level `PillProgressView.kt` (custom View).

These are the *code* behind the design skills (`m3e-animation-standards`,
`settings-page-standards`, etc.) — the skills explain intent, `shared/android/` is the impl.

## Rules
- **Edit the canonical in `hora-core/shared/android/`**, then re-run the sync in each app.
  **Never hand-edit the generated copy inside an app** — it is overwritten on next sync and
  carries a "do not hand-edit" header + a `.hora-core-synced-android` provenance manifest.
- Kotlin declares `package __HORA_PKG__.util` (and `import __HORA_PKG__.Constants` where
  needed); the sync rewrites `__HORA_PKG__` to the app's base package. Resources are copied
  verbatim. `ChipHelper` calls `ThemeHelper` from the same package.
- A consuming app must ship `res/font/google_sans_flex` and a `Constants` with
  `ANIM_DURATION_LONG`, `ANIM_DURATION_EXTRA_LONG`, `ANIM_STAGGER_BASE_DELAY`.

## How to consume (any app)
1. Copy `templates/sync_shared_android.sh` → `android/tools/sync_shared_android.sh`; set
   `APP_PKG` (e.g. `com.hora.varisankya`).
2. `bash android/tools/sync_shared_android.sh` (from repo root) → copies resources, rewrites
   the Kotlin package, writes the provenance manifest.
3. Build. Pathivu is the reference consumer.

## Adding a new shared component
Put the canonical under `shared/android/{res,kotlin}/`, add it to both the README table and
the `RES_FILES`/`KT_FILES` arrays in `templates/sync_shared_android.sh` (and each app's copy),
then re-sync. Only promote things that are genuinely identical across apps (diff first,
normalizing the package). Example: the `Widget.App.*` / `ShapeAppearance.App.*` styles in
`styles_shared.xml` were extracted only after confirming 26 of them were byte-identical
across both apps — the 4 that diverged (text-field box style, destructive button) stayed
app-local. Same bar applies to anything new.
