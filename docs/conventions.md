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

`hora-core` mostly shares documentation and assets, consumed by reference. The first
extracted **code** module — `brand/notification-icon/gen_notification_icon.py` — is a
dev-time generator, not a runtime dependency, so its consumption mechanism is **copy
locally and customize**: each app pastes the script into its own `android/tools/` and
swaps the glyph constant. This sidesteps the cross-language code-gen question above
entirely, since nothing is compiled or imported across apps. If a future module needs
real code sharing (a runtime library, not a generator), decide then between a git
submodule and a published artifact, and record the decision here.

`templates/shared-firebase/` is consumed the same way — **copy locally and
customize**: paste it into the new app's `shared/firebase/`, rename `.example`, edit
the project-ID comment. It's a starting point for a new app's own files, not something
an existing app re-syncs against, so there's no ongoing-consumption question to decide.

Shared **agent skills** are the one module with *ongoing* consumption rather than a
one-time copy: they're synced (not hand-copied) via `templates/sync-shared-skills/`, so
re-running the script re-pulls the latest from hora-core. See "Agent skills" above.
