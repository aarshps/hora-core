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

### Firebase contract folder

`shared/firebase/firebase.json` + `firestore.rules` is boilerplate enough to template:
every family app so far is a single signed-in user with full read/write access to
their own `/users/{userId}` subtree, nothing else. [`templates/shared-firebase/`](../templates/shared-firebase/)
has a ready-to-copy `firebase.json` and a `firestore.rules.example` implementing that
rule, plus a commented-out optional extension for apps that also need a
collection-group "read across my own subcollections" query. Copy it into a new app's
`shared/firebase/`, rename the `.example`, and fill in the project ID comment — there
is nothing else to customize unless the app's access model is genuinely not
per-user-only.

### Domain spec + golden-vector parity testing

Each app's `shared/domain/SPEC.md` is the canonical, prose description of that app's
data model and business rules (field names/types/defaults, the data layout, and the
non-obvious behavioural rules — e.g. how a "mark done" action mutates state). Each
platform (Kotlin/Swift/TypeScript) re-implements the spec natively — see "Cross-language
code sharing" below for why it's re-implemented rather than shared as compiled code.
`shared/domain/golden-vectors.json` is what keeps the three re-implementations honest:
language-neutral input/output pairs for every pure function described in the spec
(date math, formatting, derived state), which each platform loads into its own test
suite and asserts against. A platform's port is only "done" once it passes the same
golden vectors as the others. This SPEC.md + golden-vectors.json pair is the shared
**pattern** every app should use; the actual spec and vectors are app-specific business
logic and are not templated here — see `templates/README.md`.

## App versioning

One scheme across the family (reference: Varisankya), so every app's About screen, git tags, and
Play release-notes read the same way:

- **`versionName`** carries the channel:
  - **beta:** `MAJOR.MINOR-beta.N` — e.g. `3.9-beta.9`, `1.0-beta.37`. `N` increments per beta build
    of that `MAJOR.MINOR`.
  - **stable:** `MAJOR.MINOR` (drop the suffix) — e.g. `3.8`.
- **`versionCode`** is a **monotonic integer, +1 for every build that reaches any Play track**
  (internal counts). Never reused or decreased, and **decoupled** from `versionName` — one
  `MAJOR.MINOR` line spans many betas, each its own code.
- **Git tag** = `v<versionName>` — `vMAJOR.MINOR-beta.N` for a beta, `vMAJOR.MINOR` for a stable cut.
  One tag per shipped build.
- **Bumping:** a new feature line bumps `MINOR` (or `MAJOR`) and resets to `-beta.1`; otherwise just
  `-beta.(N+1)`. `versionCode` is +1 either way.
- Each shipped build gets a Play **release-notes** file
  (`src/main/play/release-notes/<locale>/<track>.txt`, ≤ 500 chars, plain ASCII).

`hora-app-release` defers the numbers to this scheme; each app's `CLAUDE.md` "current version" line
records the last shipped `versionName` / `versionCode` and the next free code.

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

### Local build environment (Windows)

Across family apps built on this machine: JDK 17 (Temurin) and the Android SDK at
`C:\Users\Aarsh\AppData\Local\Android\Sdk`. A fresh app checkout's `android/local.properties`
needs `sdk.dir=` pointed at that path (plus signing properties — see Secrets below);
the file is gitignored per-app and not templated here since it's machine-, not
family-, specific.

## Agent skills

Shared skills live in this repo at `.github/skills/<name>/SKILL.md` — that's the
canonical location for family-wide skills, resolving the location question that
otherwise varies per app (Pathivu uses `.claude/skills/`, Varisankya uses
`.agent/skills/`). Apps keep their own existing local directory convention for
app-specific skills; only pull a skill into `.github/skills/` here once it's
generalized for 2+ apps (see `agent-skill-standards`).

**Consumption:** apps don't read these skills across repos — an agent working inside an
app checkout only sees that app's own skill dir. So each app runs a small **sync
script** (see [`templates/sync-shared-skills/`](../templates/sync-shared-skills/)) that
copies the shared skills it uses from a local hora-core checkout into its native skill
dir. The synced copies are **generated**: edit the canonical skill here in hora-core and
re-run the script — never hand-edit the copy in an app. This is what lets an app dedup
its old hand-maintained duplicates against hora-core without losing local discoverability.
When copying the script in, the app must also add `*.sh text eol=lf` to its
`.gitattributes` (hora-core ships this guard) — otherwise a fresh Windows clone with
`core.autocrlf=true` rewrites the script to CRLF and `bash` fails on the `\r`.

## Shared Android source

[`shared/android/`](../shared/android/README.md) is the canonical home for Android
building blocks two or more apps use **verbatim** — `res/values/dimens.xml`,
`res/values/type.xml` (`TextAppearance.App.*`), `res/values/styles_shared.xml` (the
byte-identical `Widget.App.*` / `ShapeAppearance.App.*` widget & shape styles),
`res/values/colors.xml` (the `mono_*` monochrome palette), `res/values/ids.xml`,
`res/values/attrs.xml`, the chip color selectors (+ `chip_stroke_app` / `outline_stroke_app`),
the `res/anim/slide_*` nav transitions, `res/values-night/colors.xml` (dark palette), the
**brand font** `res/font/google_sans_flex.xml` (+ variable `.ttf`), the `res/xml/*` backup
policy, the generic shape drawables + the shared `res/drawable/ic_*` icon set, and
`util/ChipHelper.kt` / `ThemeHelper.kt` / `AnimationHelper.kt` / `TimeProvider.kt` plus the
top-level `PillProgressView.kt`. Each
app keeps its own `themes.xml` for app-specific theme config + any styles that genuinely
diverge between apps. Unlike a doc skill (which
explains *intent*), this folder is the *code itself*. The paired `.github/skills/`
entries (`m3e-animation-standards`, `settings-page-standards`, …) describe the why.

**Consumption (same generated-copies model as skills):** an app copies
[`templates/sync_shared_android.sh`](../templates/sync_shared_android.sh) into
`android/tools/`, sets `HORA_CORE`/`APP_PKG`, and runs it. The script copies resources
verbatim, rewrites the Kotlin package placeholder `__HORA_PKG__` → the app's base
package, and writes a `.hora-core-synced-android` provenance manifest. Edit a shared file
here in hora-core and re-run the sync in each app — never hand-edit the generated copy.
The brand font now ships from here (`res/font/google_sans_flex` + the variable `.ttf`); the
## Shared Web source

[`shared/web/`](../shared/web/README.md) is the canonical home for the Web building blocks every Hora web app shares **verbatim**: the design-system stylesheet (`res/css/web_shared.css` — the `--md-*` → role-token mapping, Tailwind `@theme` aliases, shape radii matching Android dimens, and the `.card`/`.item-*`/`.sheet`/`.pill-*`/`.chip` utilities) plus a set of presentational React components — `ServiceWorker`, `Sheet`, `controls` (Button/Switch/Field/TextInput/Select/Segmented), `SignIn`, `ConfirmDialog`, `AboutSheet`, the settings primitives (`settings.tsx`: SettingsSection/SectionLabel/Row/Toggle/Divider/LinkRow), `EmptyState`, and `ScreenHeader`. It also ships one framework-agnostic web util — the M3E haptics factory `lib/haptics-core.ts` (`createHaptics(isEnabled)`; each app injects its own "haptics enabled" pref via a one-line local `lib/haptics.ts`, so the shared file stays free of app storage keys). The components are prop-driven and free of app-specific strings/logic; the CSS references only `--md-*` / role tokens. Bar for inclusion is the family standard: **2+ apps use it verbatim**.

**Consumption:** an app copies [`templates/sync_shared_web.sh`](../templates/sync_shared_web.sh) into `web/scripts/sync_shared_web.sh`, sets `HORA_CORE`/`APP_NAME`/`WEB_APP_ROOT`, and runs it. The script copies each file in its `FILES` map (CSS → `web/app/`, components → `web/components/`), prepends a generated-file header (after the `"use client"` directive where present), rewrites the optional `__HORA_APP_NAME__` token, and records a `web/.hora-core-synced-web` provenance manifest. The app's `globals.css` keeps the three-layer `@import "tailwindcss"; @import "./theme.css"; @import "./web_shared.css";` chain. Edit a shared file in `hora-core` and re-run the script in each app — never hand-edit the generated copy.

## Shared iOS source

[`shared/ios/swift/`](../shared/ios/README.md) is the canonical home for Swift used **verbatim**
(modulo one display-name token) by 2+ Hora apps — the SwiftUI counterpart of the Android shared
layer. Today: `Haptics.swift` (M3E haptic helper), `BiometricAuth.swift` (App-Lock / LocalAuthentication
wrapper), `SelectionSheet.swift` (glass single-choice picker — the counterpart of Android's
`SelectionBottomSheet`).

**Consumption:** an app copies [`templates/sync_shared_ios.sh`](../templates/sync_shared_ios.sh)
into `ios/tools/sync_shared_ios.sh`, sets `HORA_CORE`/`APP_NAME`/`IOS_APP_ROOT`, and runs it. The
script writes each file to its mapped path under the app's iOS source root, rewriting the
`__HORA_APP_NAME__` token to the app's display name, and records provenance in
`ios/tools/.hora-core-synced-ios`. Generated copies carry a "do not hand-edit" header; edit the
canonical file in `hora-core` and re-run. The app's iOS target uses XcodeGen, so the files compile
in place at their existing paths (no project edit needed); CI (`ios-build.yml`) validates the build.

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

### App icons (launcher, notification, iOS, web, Play)

Every family icon — launcher foreground/legacy/round/monochrome, the notification
status-bar icon, the iOS AppIcon, web favicon/PWA icons, and the Play 512 — is
generated from **one engine and one spec**: the app's Malayalam wordmark set in
**Baloo Chettan 2** (700), slate `#445353` on near-white `#FCFCFC`, shaped with
harfbuzz and rasterised by FreeType (so self-intersecting glyphs like ത fill with no
holes). The notification icon is specifically a **solid white disc with the app's
Malayalam initial knocked out as a hollow** (single `evenOdd` path) drawn from the same
Baloo glyph. Canonical standard, generator, and per-app config live in
[`brand/launcher-icon/`](../brand/launcher-icon/README.md). These are firm family
conventions, not hedged references — do not revert to hand-authored raster tuning, nor
to a framed or stroked-glyph notification treatment.

## Cross-language code sharing

No cross-language code generation. Kotlin/Swift/TypeScript do not share compiled code
(KMP and a shared-TS core are out of scope). Shared **logic** is expressed as a domain
spec + golden test vectors, not generated code. Shared **assets and conventions** live
here in `hora-core`.

## Secrets

Secrets are managed with the **Bitwarden CLI (`bw`)**, never committed. On Windows `bw`
is at `C:\Users\Aarsh\AppData\Roaming\npm\bw.cmd`. `hora-core` is public and must never
contain secrets of any kind.

### Disaster-recovery & secret-retrieval convention

Every family app follows the same shape for secret storage and recovery (each app's
own `DISASTER_RECOVERY.md` has the literal, app-specific runbook — this is the
convention behind it, generalized so it can live in a public repo):

- **The Bitwarden master password is the recovery seed**, settled as an ADR in each
  app, not re-litigated per session. It is held by the developer offline (memory /
  physical backup), not just on disk.
- **A gitignored `.env` at the repo root** holds `BW_CLIENTID`, `BW_CLIENTSECRET`, and
  `BW_PASSWORD` so agents/CI can unlock the vault non-interactively. Always
  `chmod 600 .env`. A committed `.env.example` documents the keys without values.
  This is an accepted, intentional tradeoff (agent ergonomics vs. single-factor-on-disk
  risk, mitigated by full-disk encryption + the master password also living outside
  the disk) — don't relitigate it in review; if a new risk genuinely changes the
  calculus, raise it as an issue rather than inline.
- **One unlock helper, sourced, not run:** `source scripts/bw_unlock.sh` exports a
  `BW_SESSION` into the current shell. Per-platform `retrieve_secrets.sh` scripts
  (e.g. `android/retrieve_secrets.sh`) then read specific Bitwarden item fields and
  write them to the local files the build actually needs (`google-services.json`,
  the upload keystore, `local.properties` signing properties, etc.) — never to git.
- **One Bitwarden vault item per app** (plus one for any per-platform signing
  material, e.g. "`<App> iOS signing`"), with one field per secret. Large binaries
  (keystores, base64 configs) that exceed Bitwarden's field-size limit are split
  across `[Part 1]` / `[Part 2]` fields and reassembled by the retrieval script.
- **CI mirrors the same fields as GitHub Secrets** where a workflow can't shell out to
  `bw` directly (mainly iOS signing); a `check_*_secrets.sh` style script verifies
  Bitwarden and GitHub Secrets agree.
- **A recovery-acceptance test** is the actual spec for "is DR documented enough": on
  a fresh machine with only the master password, clone → `.env` → `bw_unlock.sh` →
  `retrieve_secrets.sh` should be sufficient, with no other tribal knowledge required.
- **Operational hygiene to carry over per app:** a monthly encrypted `bw export`
  stored offline, a documented per-scenario runbook (lost dev machine / lost
  Bitwarden / lost platform-vendor account / lost GitHub / founder bus-factor), and
  Bitwarden Emergency Access configured for a trusted contact.

## Module consumption (decide per module as they're added)

`hora-core` mostly shares documentation and assets, consumed by reference. The
**icon engine** — `brand/launcher-icon/gen_launcher_icon.py` — is a dev-time generator,
not a runtime dependency, so the cross-language code-gen question above does not apply.
Its consumption model is **run centrally from a hora-core checkout**: the per-app `APPS`
config (Malayalam wordmark, initial, repo path, iOS module dir) lives in the script, and
`python gen_launcher_icon.py <app>` writes the full generated asset set directly into
that app's tree. The generated icons are outputs — re-run the engine to update them;
never hand-tune them in the app (same "generated copies" discipline as skills and shared
Android source). If a future module needs real code sharing (a runtime library, not a
generator), decide then between a git submodule and a published artifact, and record the
decision here.

`templates/shared-firebase/` is consumed the same way — **copy locally and
customize**: paste it into the new app's `shared/firebase/`, rename `.example`, edit
the project-ID comment. It's a starting point for a new app's own files, not something
an existing app re-syncs against, so there's no ongoing-consumption question to decide.

Shared **agent skills** and **shared Android source** are the modules with *ongoing*
consumption rather than a one-time copy: each is synced (not hand-copied) from a local
hora-core checkout via a small per-app script — `templates/sync-shared-skills/` for
skills, `templates/sync_shared_android.sh` for `shared/android/` — so re-running the
script re-pulls the latest from hora-core. See "Agent skills" and "Shared Android
source" above.
