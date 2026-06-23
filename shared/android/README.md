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
| `res/values/styles_shared.xml` | `…/res/values/styles_shared.xml` | the byte-identical M3E `Widget.App.*` / `ShapeAppearance.App.*` / `App.*` widget & shape styles. App-specific theme config + divergent styles stay in the app's own `themes.xml` |
| `res/values/colors.xml` | `…/res/values/colors.xml` | the family **monochrome palette** (`mono_*`, light + dark tonal layers) + M3 drawable colour mappings |
| `res/values/ids.xml` | `…/res/values/ids.xml` | shared resource IDs (the `haptic_scroll_listener_tag` the scroll-haptics helper uses) |
| `res/values/attrs.xml` | `…/res/values/attrs.xml` | theme attrs (placeholder — empty today; kept shared so a future family attr lands in one place) |
| `res/color/chip_background_color.xml` | `…/res/color/…` | chip selector — selected = tertiary, unselected = surfaceContainerHigh |
| `res/color/chip_text_color.xml` | `…/res/color/…` | chip selector |
| `res/color/chip_stroke_color.xml` | `…/res/color/…` | chip selector — tertiary border when unselected |
| `res/color/chip_stroke_app.xml` | `…/res/color/…` | chip-stroke selector (app-styled variant) |
| `res/color/outline_stroke_app.xml` | `…/res/color/…` | outline-stroke selector (focused / unfocused) |
| `res/anim/slide_{in,out}_{left,right}.xml` | `…/res/anim/…` | M3 slide transitions for activity / sheet navigation |
| `kotlin/util/ChipHelper.kt` | `…/java/<pkg>/util/ChipHelper.kt` | selected = primary squircle, unselected = bordered pill |
| `kotlin/util/ThemeHelper.kt` | `…/java/<pkg>/util/ThemeHelper.kt` | resolve M3 color attrs at runtime |
| `kotlin/util/AnimationHelper.kt` | `…/java/<pkg>/util/AnimationHelper.kt` | M3 emphasized interpolators + helpers; needs the app's `Constants.ANIM_*` |
| `kotlin/util/TimeProvider.kt` | `…/java/<pkg>/util/TimeProvider.kt` | injectable time source (today / now) for testable date logic |
| `kotlin/PillProgressView.kt` | `…/java/<pkg>/PillProgressView.kt` | custom pill-shaped progress `View` (colours via `ThemeHelper`) |

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

## `styles_shared.xml` — what's in vs. out

Landed 2026-06-23 (Varisankya was the first to extract; Pathivu still has the
duplicated copies and adopts on its next pass). The file holds the **26 widget &
shape styles that are byte-identical across the apps** — `Widget.App.{AppBarLayout,
Toolbar,SearchView,BottomSheet.Modal,Chip,Switch,Slider,Slider.Tooltip,Button,
Button.Outlined,Button.Tonal,Button.Tertiary}`, `ShapeAppearance.App.{Button,
BottomSheet,Chip.Selected,Chip.Unselected,FirstItem,MiddleItem,LastItem,SingleItem}`,
and `App.{ShapeAppearanceOverlay.Rounded,ShapeAppearanceOverlay.Pill,ButtonToggleGroup,
ButtonToggleGroup.Rounded,Button.Destructive.Icon,Button.Success}`.

**Deliberately left in each app's `themes.xml`** (not byte-identical — real per-app
design choices, do not force-share): `Theme.*` (app theme + splash), and the styles
where the apps diverge — `App.ShapeAppearanceOverlay.TextField` (4dp vs 14dp),
`App.TextInputLayout.Rounded{,.ExposedDropdownMenu}` (outlined vs filled box), and
`App.Button.Destructive` (outlined-error vs tonal). Before adding a style here, confirm
it is identical in 2+ apps (`norm`-compare the `<style>` bodies).
