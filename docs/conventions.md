# Hora family conventions

The shared stack and conventions every Hora app is expected to follow. This is the
single source of truth; when a convention changes, update it here.

## App shape

Each Hora app is a **cross-platform monorepo** with up to three platforms plus a
shared contract folder:

```
<app>/
├── android/    Kotlin + Gradle
├── ios/        SwiftUI + XcodeGen
├── web/        Next.js (App Router) + TypeScript
└── shared/
    ├── firebase/   firestore.rules, firebase.json, .firebaserc
    └── domain/     SPEC.md (canonical data model) + golden-vectors.json
```

Each app talks to its **own** Firebase project. The Firestore data model is kept
identical across an app's platforms via that app's `shared/domain/SPEC.md` — field
names, types, and layouts must match across Android/iOS/web.

## Android stack (reference — confirm against the app's `libs.versions.toml`)

As of the most recent family app (Varisankya):

| Component | Version |
| --- | --- |
| Android Gradle Plugin | 9.0.1 |
| Kotlin | 2.3.0 |
| Material | Material 3 Expressive |
| Min/target | Android 15+ |
| Architecture | MVVM |
| Play publishing | `com.github.triplet.play` (gpp) |

Apps pin versions in `android/gradle/libs.versions.toml`. Treat the table above as a
starting reference, not a hard pin — always read the consuming app's catalog.

## Design tokens (reference — confirm against the app's design-system doc)

As of the most recent family app (Varisankya), Android uses Material 3 Expressive
with these constants. Treat as a starting reference, not a hard pin — each app's own
design-system doc is authoritative:

| Token | Value | Use |
| --- | --- | --- |
| Corner radius — large | 28dp | Hero cards, bottom-sheet content, single/first/last grouped-list items |
| Corner radius — medium | 24dp | Filled buttons |
| Corner radius — small | 12dp | Middle items in grouped lists |
| Pill shape | 100dp | Force-rounded chips/status pills |
| Animation — short | 100–200ms | Rapid snaps / interactive-press recovery |
| Animation — medium | 300–400ms | Standard layout state changes |
| Animation — long | 500ms | Activity/fragment shared-axis transitions, large list entrances |
| Screen transition | `MaterialSharedAxis.Z` | Primary navigation between screens |
| Type | Google Sans Flex (native), Nunito (closest open web equivalent) | App-wide type family |

Web apps seed their Material 3 palette from the app's own brand icon color via
Material Color Utilities (`SchemeTonalSpot`) rather than wallpaper-based Dynamic
Color, since a browser has no wallpaper — each app picks its own seed color.

### Notification status-bar icon

Every app's notification-shade icon is a **solid round (filled white disc) with the
app's Malayalam initial knocked out as a hollow**, as a single `evenOdd` vector path.
Canonical standard, generator, and per-app instructions live in
[`brand/notification-icon/`](../brand/notification-icon/README.md). This is a firm
family convention, not a hedged reference — do not revert to a framed or
stroked-glyph treatment.

## Cross-language code sharing

No cross-language code generation. Kotlin/Swift/TypeScript do not share compiled code
(KMP and a shared-TS core are out of scope). Shared **logic** is expressed as a domain
spec + golden test vectors, not generated code. Shared **assets and conventions** live
here in `hora-core`.

## Secrets

Secrets are managed with the **Bitwarden CLI (`bw`)**, never committed. On Windows `bw`
is at `C:\Users\Aarsh\AppData\Roaming\npm\bw.cmd`. `hora-core` is public and must never
contain secrets of any kind.

## Module consumption (decide per module as they're added)

`hora-core` mostly shares documentation and assets, consumed by reference. The first
extracted **code** module — `brand/notification-icon/gen_notification_icon.py` — is a
dev-time generator, not a runtime dependency, so its consumption mechanism is **copy
locally and customize**: each app pastes the script into its own `android/tools/` and
swaps the glyph constant. This sidesteps the cross-language code-gen question above
entirely, since nothing is compiled or imported across apps. If a future module needs
real code sharing (a runtime library, not a generator), decide then between a git
submodule and a published artifact, and record the decision here.
