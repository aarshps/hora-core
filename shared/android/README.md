# shared/android — Hora-family shared Android source

Canonical source for the Android building blocks every Hora app (Pathivu, Varisankya,
future siblings) shares **verbatim**. Each app consumes these by copying them in with a
small per-app sync script — there is no published artifact; the family's mechanism is
"generated copies from hora-core" (the same model as `.github/skills/`).

**Golden rule:** edit a shared file **here**, then re-run the sync in each app. Never
hand-edit the generated copy inside an app (it is overwritten on the next sync).

## What's shared

| File | Consumed as | Notes |
|------|-------------|-------|
| `res/values/dimens.xml` | `app/src/main/res/values/dimens.xml` | card radii, group/section spacing, card padding |
| `res/values/type.xml` | `…/res/values/type.xml` | `TextAppearance.App.*` (forces `@font/google_sans_flex`) |
| `res/color/chip_background_color.xml` | `…/res/color/…` | chip selector — selected = tertiary, unselected = surfaceContainerHigh |
| `res/color/chip_text_color.xml` | `…/res/color/…` | chip selector |
| `res/color/chip_stroke_color.xml` | `…/res/color/…` | chip selector — tertiary border when unselected |
| `kotlin/util/ChipHelper.kt` | `…/java/<pkg>/util/ChipHelper.kt` | selected = primary squircle, unselected = bordered pill |
| `kotlin/util/ThemeHelper.kt` | `…/java/<pkg>/util/ThemeHelper.kt` | resolve M3 color attrs at runtime |
| `kotlin/util/AnimationHelper.kt` | `…/java/<pkg>/util/AnimationHelper.kt` | M3 emphasized interpolators + helpers; needs the app's `Constants.ANIM_*` |

These pair with the documentation skills in `.github/skills/` (`m3e-animation-standards`,
`settings-page-standards`, etc.) — the skills explain the *intent*, this folder is the *code*.

## The package placeholder

Kotlin files declare `package __HORA_PKG__.util` (and import `__HORA_PKG__.Constants`
where needed). The sync rewrites `__HORA_PKG__` → the app's base package
(`com.hora.pathivu`, `com.hora.varisankya`, …). Resources are package-independent and
copied verbatim. `ChipHelper` references `ThemeHelper` from the same package (no import).

## How an app consumes this

1. Copy `templates/sync_shared_android.sh` (below) into the app as
   `android/tools/sync_shared_android.sh` and set the three values at the top:
   `HORA_CORE` (local checkout path), `APP_PKG` (e.g. `com.hora.varisankya`),
   and the `res`/`java` roots if they differ.
2. Run `bash android/tools/sync_shared_android.sh`. It copies the resources verbatim,
   rewrites the Kotlin package, and writes a `.hora-core-synced-android` provenance
   manifest (source path, timestamp, hora-core commit).
3. The app must already ship `res/font/google_sans_flex` and a `Constants` with
   `ANIM_DURATION_LONG`, `ANIM_DURATION_EXTRA_LONG`, `ANIM_STAGGER_BASE_DELAY`.

Pathivu's `android/tools/sync_shared_android.sh` is the reference implementation.

## Roadmap (next things to pull in here)

These are byte-identical across the apps today but still embedded in each app's
`themes.xml`; extract them into a shared `res/values/styles_shared.xml` next:
`Widget.App.Chip`, `Widget.App.Switch`, `Widget.App.Button{,.Outlined,.Tonal}`,
`Widget.App.Slider`, and `ShapeAppearance.App.{Chip.*,Button,FirstItem,MiddleItem,LastItem,SingleItem}`.
Doing so needs care (themes.xml also holds app-specific theme config), so it's staged
as a follow-up rather than risking both apps' theme files in one pass.
