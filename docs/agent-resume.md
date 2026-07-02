# Agent Resume — hora-core

## Start here

- Read `AGENTS.md`, then this file.
- Open only the relevant skill under `.github/skills/`.
- Any Hora app agent may commit to `main` and update the wiki (`master`) directly — see
  `AGENTS.md` § Working agreements. There is no agent-to-agent coordination channel; this
  file is the shared, committed record. Append a dated entry when you make a lasting
  decision.
- GitHub: use plain `gh` (authenticated as `aarshps` on this machine). Verify with
  `gh api user --jq .login` if it matters.

## Repo map

- `brand/` — shared visual identity for the whole family.
- `docs/conventions.md` — the shared stack and conventions every Hora app follows.
- `docs/agent-resume.md` — this file (durable state + handoff notes).
- `.github/skills/` — agent skills shared across the family.

## Durable repo state — as of 2026-06-16

- **Repurposed.** This repo previously held a decommissioned .NET + Angular project
  (`Hora.App`/`Hora.Db`/`Hora.Sv`). That project was removed and the repo was
  re-purposed as the shared-code home for the Hora **Android/multiplatform** app family.
- **Unarchived.** The GitHub repo was archived (read-only) and has been unarchived so
  it can be written to again. Default branch: `main`. Wiki default branch: `master`.
- **Auth is local to this machine.** Plain `gh` resolves to `aarshps` via keyring. The
  old Mac wrapper `scripts/gh-aarshps` (pointing at `/Users/aps/.../.gh-aarshps`) was
  removed — it never existed on this Windows machine.
- **Public repo** — no secrets, ever.
- **First shared assets landed (same day, later pass):** the notification-icon
  standard + generator (`brand/notification-icon/`, extracted from Varisankya, which
  was the first app to need it) and the `agent-skill-standards` skill. Pulled in by an
  agent working from the Varisankya side after the user asked for cross-app
  coordination — there's no live inter-session messaging available, so coordination
  happened by reading this repo's own `AGENTS.md`/`conventions.md`/this file as the
  shared source of truth, same as any other agent would. Also added a hedged "Design
  tokens (reference)" table to `conventions.md` (shape/motion/type constants) sourced
  from Varisankya's design-system doc.
- **Deliberately left out of this pass:** Varisankya's other Android skills
  (`m3-dynamic-colors`, `m3e-animation-standards`, `m3e-haptic-standards`,
  `skeleton-loading-standards`, `app-performance-standards`, `android-15-standards`)
  were reviewed but NOT copied here — they're written in Varisankya's voice with
  concrete class/package names (`ThemeHelper.kt`, `com.hora.varisankya`), and one
  (`m3-dynamic-colors`) describes a hybrid monochrome/dynamic-color split that the
  app's own wiki says was reverted in v3.8-beta.9, i.e. it's stale. Don't copy these
  in verbatim; if/when a second app needs the same underlying rule, generalize it
  fresh rather than porting the Varisankya-specific text.
- **Ops/contract patterns landed (same day, third pass):** added `templates/` —
  `shared-firebase/firebase.json` + `firestore.rules.example`, generalized from
  Varisankya's and Pathivu's near-identical real Firebase contract files (both are a
  single signed-in user with full read/write on their own `/users/{userId}` subtree).
  `docs/conventions.md` gained three new subsections: "Firebase contract folder"
  (points at the new template), "Domain spec + golden-vector parity testing"
  (documents the `SPEC.md` + `golden-vectors.json` methodology as prose-only — each
  app's actual spec/vectors are business logic and are NOT templated), and
  "Disaster-recovery & secret-retrieval convention" (generalized from both apps'
  `DISASTER_RECOVERY.md`: Bitwarden-as-source-of-truth, gitignored `.env` +
  `bw_unlock.sh`, per-platform `retrieve_secrets.sh`, one-vault-item-per-app with
  `[Part N]` splitting, GitHub Secrets mirroring, recovery-acceptance test). Also
  fixed a stale `README.md` line that still listed Pathivu as three separate repos
  (`pathivu-android`/`-ios`/`-web`) instead of its actual current monorepo shape.
  Not pulled in: Pathivu's `pathivu-android/_tools/` icon-gen scripts
  (`match_icon.py`/`gen_icons.py`) — that directory also contains unrelated
  experiment binaries and a plaintext keystore-password file, so it needs a clean
  manual extraction, not a directory copy, and the "reconcile skill location"
  question from Pathivu's `HORA_CORE_HANDOFF.md` (`.claude/skills/` vs.
  `.agent/skills/` vs. this repo's `.github/skills/`) — still open.
- **Skills landed (same day, fourth pass):** merged and generalized five skills into
  `.github/skills/` from Pathivu's `.claude/skills/`, Varisankya's `.agent/skills/`,
  and two machine-local global skills — `hora-app-release` (merged Pathivu's release
  procedure + the global generic skeleton + Varisankya's track-gating/launch-day
  logic into one 12-step procedure), `hora-play-store` (Play Console specifics: the
  App Signing SHA fix for "no Google account" sign-in failures, store-icon-vs-
  launcher-icon distinction generalized away from Varisankya's hardcoded metrics,
  track promotion + launch-day exception, blocked-listing-API manual workaround),
  `hora-bitwarden-secrets` (Varisankya's real workflow, fully scrubbed of vault item
  names, folder names, and a real test-account email before writing into this public
  repo), `agent-session-closing` (near-verbatim 5-step closing checklist), and
  `hora-launcher-icon` (the Malayalam-wordmark icon-generation method — graft shared
  subglyph, render letters separately, match stroke weight by uniform trim, match
  height then fit bounding circle, assemble with gap after stroke-restore — written
  as method-only, no scripts copied in). Resolved the "reconcile skill location"
  question above: this repo canonically uses `.github/skills/`; apps keep their own
  local convention. Folded Varisankya's `headless-linux-builds` environment facts
  (JDK 17 Temurin, Windows SDK path) into `conventions.md`'s Android-stack section
  instead of writing a standalone skill for them.
  **Deliberately deferred:** Varisankya's `app-readiness-policy`,
  `m3e-animation-standards`, `m3e-haptic-standards`, and `skeleton-loading-standards`
  — all written against concrete Varisankya classes/APIs (`calculateHeroData`,
  `AnimationHelper`, `PreferenceHelper`), not yet generalized. Pathivu's
  `_tools/` icon-gen scripts (`match_icon.py`/`gen_icons.py`/`final_proof.py`/
  `render_pata.ps1`) were not copied — same reasoning as the third pass above (mixed
  with throwaway experiment files and plaintext-looking secret files); the new
  `hora-launcher-icon` skill captures the method instead.

- **Cross-session mailbox added (same day, fifth pass):** added `.agent-mailbox/`
  (gitignored, same-machine only) plus the `hora-agent-mailbox` skill documenting the
  protocol (one folder per repo slug, write-once timestamped messages,
  `from`/`to`/`status` frontmatter, `open`/`resolved` flow). This supplements, not
  replaces, the durable record in this file — mailbox messages are ephemeral pings,
  not the source of truth. Bootstrapped with a first message in
  `.agent-mailbox/hora-core/` announcing the skills/templates extraction above to
  Pathivu's and Varisankya's agents, since Pathivu's own `HORA_CORE_HANDOFF.md`
  describes an adoption plan (consume → delete local duplicate → verify build) that
  needs exactly this kind of landed-and-ready signal.

- **Swipe-action standard added (2026-06-18):** `m3e-swipe-standards` skill in
  `.github/skills/` captures the family's list swipe-to-act behaviour — the sticky + haptic +
  natural-recover gesture (`SwipeActionCallback : ItemTouchHelper.SimpleCallback`) AND the
  wiring rule that stops a kept (non-removed) row from sticking off-screen: a SYNCHRONOUS
  `notifyItemChanged` + fire the data write only AFTER the spring-back settles (a confirmation
  sheet, or event-based `recyclerView.postOnAnimation { itemAnimator.isRunning { ... } }`) —
  never an immediate async write, never a fixed delay (it races on slow devices). Added by the
  Pathivu agent (user authorized direct hora-core edits) after Pathivu's swipe took several
  betas to get right; Varisankya is the reference impl and both apps follow it.

- **Unified icon engine + shared Android source landed (2026-06-22).** Three commits moved
  hora-core from "docs + assets" toward a real shared-source library. Where an earlier
  entry conflicts, treat the following as current:
  - **`settings-page-standards` skill** (`2022757`) — family Settings design language, added
    to `.github/skills/` as a sync candidate for both apps.
  - **`shared/android/` shared source** (`d3dc252`) — the first byte-identical Android
    *code + resources* shared verbatim (`dimens.xml`, `type.xml`, chip-color selectors +
    `ChipHelper`/`ThemeHelper`/`AnimationHelper.kt`; Kotlin carries a `__HORA_PKG__`
    package placeholder rewritten on sync). Consumed via `templates/sync_shared_android.sh`
    — same generated-copies discipline as skills (edit here, re-run, never hand-edit the
    copy). Documented in the `shared-android-source` skill + `conventions.md` ("Shared
    Android source"). Its README stages a follow-up: extract the byte-identical
    `Widget.App.*` / `ShapeAppearance.App.*` styles out of each app's `themes.xml` into a
    shared `styles_shared.xml` next (separate pass because `themes.xml` also holds
    app-specific config).
  - **Unified Baloo Chettan 2 icon engine** (`7f23dc1`) — `brand/launcher-icon/gen_launcher_icon.py`
    generates EVERY icon for an app (launcher all densities + monochrome + legacy/round,
    notification disc-knockout, iOS AppIcon, web favicon/PWA, Play 512) from one spec: the
    app's Malayalam wordmark in Baloo Chettan 2 700, harfbuzz-shaped + FreeType-rasterised
    (nonzero fill → no holes in ത). Run from a hora-core checkout (`python
    gen_launcher_icon.py <app>`, per-app `APPS` config) writing into each app's tree. Font
    bundled (OFL).
  - **Supersessions (the history below stays accurate; these are now the live rules).** The
    engine **replaces** (a) the hand-authored / per-app raster launcher pipeline from the
    2026-06-17/18 "launcher-icon method improved" and "launcher-icon constants RESOLVED"
    entries — the `dilate_h` weight-restore + contour-smoothing steps no longer exist; the
    icon is font-rendered (the size constant carried over, `R_FRAC=0.2435`). And (b) the
    standalone notification-icon generator from "notification-icon standard ratified" — the
    disc-with-knocked-out-initial *standard itself is unchanged and still firm*, but it is
    now emitted by the one engine (`notification_icon()`), so `brand/notification-icon/` was
    **deleted** and its rationale folded into `brand/launcher-icon/README.md`.
    `conventions.md`, `brand/README.md`, and the `hora-repo-map` skill were updated to match.
  - ~~**Open for the app agents** (adoption owned per app, not done from here): sync
    `settings-page-standards` + `shared/android/` source per app.~~ **RESOLVED (2026-06-23):**
    both apps have now adopted every shared component landed in this entry — Pathivu beta.35
    (icon engine) and beta.37 (settings/shared-source/styles_shared/colors-ids-attrs);
    Varisankya beta.8 (icon engine) + beta.9 (styles_shared) + the 06-23 re-sync of
    colors/ids/attrs. See the dated 06-23 entries below.

- **Varisankya adopted the unified icon engine — all platforms (2026-06-23).** Ran
  `gen_launcher_icon.py varisankya` and shipped it: the വരി wordmark (Baloo Chettan 2 700) +
  the വ notification disc-knockout now drive Android (launcher all densities + monochrome +
  legacy/round + notification), iOS (`AppIcon-1024`), web (favicon + PWA icons) and the Play
  512. This is the **second** app on the engine (after Pathivu's പതി/പ), so the family
  standard is now validated for both wordmarks. App-side wrinkle worth flagging for the next
  sibling: Varisankya was on `.webp` launcher foregrounds + a *vector* monochrome (Pathivu
  was already raster PNG); both are superseded by the engine's PNG output and had to be
  deleted to avoid duplicate-resource collisions (`.webp`+`.png`, vector+raster same name).
  Shipped as Varisankya Android **beta.8 (vc65)** → Play Open Testing + Vercel web prod;
  Play listing 512 set via the `edits.images` API; iOS icon landed (CI green) but TestFlight
  still gated on Apple enrollment. Resolves the icon half of the "Open for the app agents"
  item above for Varisankya; the `Widget.App.*` / `ShapeAppearance.App.*` `themes.xml`
  extraction staged in that entry is still open.

- **`styles_shared.xml` extracted — shared widget/shape styles landed (2026-06-23).** Did the
  `themes.xml` extraction the icon entry left open: `shared/android/res/values/styles_shared.xml`
  now holds the **26** `Widget.App.*` / `ShapeAppearance.App.*` / `App.*` styles that were
  **byte-identical across both apps** (verified by normalising each `<style>` body and
  diffing Varisankya vs Pathivu). Added to the README table, `conventions.md`,
  `shared-android-source` skill, and the `RES_FILES` array in both
  `templates/sync_shared_android.sh` and each app's copy. **4 styles deliberately stayed
  app-local** because they genuinely diverge — `App.ShapeAppearanceOverlay.TextField` (4dp
  vs 14dp corners), `App.TextInputLayout.Rounded{,.ExposedDropdownMenu}` (Varisankya
  outlined-box vs Pathivu filled-box), `App.Button.Destructive` (outlined-error vs tonal) —
  plus all `Theme.*`. Varisankya adopted now (synced + `themes.xml` trimmed to theme +
  divergent styles; debug build green; shipped in **beta.9 / vc66** alongside removing its
  unused long-press app shortcuts). Pathivu **adopted in beta.37 / vc37** (synced + `themes.xml`
  trimmed; see the 2026-06-23 full-sweep entry below). This closes the staged follow-up.

- **Full shared-resource sweep + family versioning standard (2026-06-23).** (a) Promoted the
  remaining byte-identical `res/values/` files into `shared/android/` — `colors.xml` (the `mono_*`
  monochrome palette + M3 drawable mappings), `ids.xml` (the haptic scroll-listener tag), and
  `attrs.xml` (empty placeholder) — wired into the README table, `conventions.md`, the
  `shared-android-source` skill, and `templates/sync_shared_android.sh` `RES_FILES`. (b) **App
  versioning is now a family standard** (`conventions.md` → "App versioning", referenced from
  `hora-app-release`): `versionName` = `MAJOR.MINOR-beta.N` in beta / `MAJOR.MINOR` stable,
  `versionCode` monotonic +1, tag `v<versionName>`. Reference = Varisankya (already `3.9-beta.9`).
  Pathivu adopts both in **beta.37 / vc37** — its first build under the new `versionName` scheme
  (was a static `1.0`), plus the sync + `themes.xml` trim of its 26 duplicated styles.

- **No launcher long-press shortcuts — family behaviour (2026-06-23).** Hora apps ship **no** static
  or dynamic app shortcuts; the long-press app-icon menu stays empty. Varisankya dropped its unused
  ones in beta.9; **Pathivu removed its two (add-habit / stats) in beta.38** — deleted
  `res/xml/shortcuts.xml` + the manifest `android.app.shortcuts` meta-data + the `ACTION_*` intent
  handling in `MainActivity` + the orphaned shortcut icons/strings. Codified in the
  **`android-platform-standards`** skill (UX expectations + checklist) so every app agent sees it.

- **Rule: hora-core `main` and wiki (`master`) move together (2026-06-23).** Any app agent (Pathivu,
  Varisankya, future siblings) that pushes a change to hora-core `main` which alters what the wiki
  describes **must** update the wiki (`master`) in the **same** pass — never leave the wiki lagging
  `main`. Codified in `AGENTS.md` (Working agreements) and the `agent-session-closing` skill checklist.
  Pure internal refactors that change nothing the wiki states are exempt — verify before skipping.

- **More shared Android source promoted (2026-06-23).** Added to `shared/android/`: `util/TimeProvider.kt`
  (injectable clock), the top-level `PillProgressView.kt` (custom progress `View`; colours via the shared
  `ThemeHelper`), the four `res/anim/slide_*` M3 nav transitions, and the `chip_stroke_app` /
  `outline_stroke_app` color selectors — all byte-identical across Pathivu + Varisankya (package-
  normalised). Wired into the template + Pathivu sync, README / conventions / `shared-android-source`
  skill. Pathivu consumes them in **beta.39**. **Deferred (tracked in a GitHub issue):**
  `BiometricAuthManager` (hardcodes `"Unlock <app>"` — externalise to a string first); the ~25
  byte-identical drawables (stable assets, low drift — optional); the `google_sans_flex` font
  (licensing / redistribution check before centralising the binary in a public repo); the
  `SelectionBottomSheet` + `bottom_sheet_selection` layout (UI bundle; needs a layout-sharing pattern);
  and `BaseActivity` (references app-specific `R.style.Theme_<App>` — needs a theme-name placeholder in
  the sync).

## Decisions

- **Shared-skill consumption = per-app sync script (decided 2026-06-16 by the user).**
  The discovery gap — an agent working only inside an app checkout (Pathivu
  `android/.claude/skills/`, Varisankya `android/.agent/skills/`) doesn't see hora-core's
  `.github/skills/` — is resolved by each app running a small sync script that copies the
  shared skills it uses from a local hora-core checkout into its own skill dir. Template +
  rationale: `templates/sync-shared-skills/`; convention written up in
  `docs/conventions.md` ("Agent skills"). Synced copies are generated (edit in hora-core,
  re-run; never hand-edit in the app). Rejected alternatives: leave-as-duplicates
  (drift), git submodule (fights each app's skill-dir convention, heavier).
- **App-side adoption is owned by each app's agent**, not done from here (hora-core does
  not write to sibling repos). Both app agents were pinged via `.agent-mailbox/` and have
  now **completed adoption** (confirmed by `resolved` mailbox replies):
  - **Pathivu** (commit on its `main`): synced `hora-app-release`, `hora-play-store`,
    `hora-launcher-icon` via the script into `android/.claude/skills/`, deleted the
    hand-maintained duplicates, folded app-specific bits into `android/CLAUDE.md`, and
    updated `HORA_CORE_HANDOFF.md` (its channel section is no longer "pending").
  - **Varisankya** (commits `88952d9` etc.): synced `agent-session-closing`,
    `agent-skill-standards`, `hora-play-store` into `android/.agent/skills/`, deleted
    `play-store-release`, documented the never-hand-edit-synced rule in its `AGENTS.md`
    (mandate 7), and now records this mailbox protocol there for future sessions.
  - Varisankya keeps `bitwarden-secrets` local (real vault names — app-specific runbook,
    not a duplicate of the scrubbed `hora-bitwarden-secrets`). Agreed.
- **Deferred UI-standard skills — four promoted and landed.** Checked Pathivu's code
  against Varisankya's deferred standards; four met the 2+ app bar (verified vs Pathivu:
  haptics in 8 files + a preference toggle, its own `util/AnimationHelper.kt`, skeleton
  layouts, `targetSdk=36` + edge-to-edge). Varisankya generalized them method-only and
  committed them to `.github/skills/` (commit `84fd531`): `m3e-haptic-standards`,
  `m3e-animation-standards`, `skeleton-loading-standards`, and `android-platform-standards`
  (the former `android-15-standards`, de-versioned to "target newest platform" per review).
  Reviewed as hora-core owner — clean, de-voiced, <=100 lines, consistent with the
  conventions.md design tokens. They are now sync candidates for both apps.
  `app-performance-standards` stays app-local (no baseline-profile evidence in Pathivu);
  `m3-dynamic-colors` / `app-readiness-policy` remain app-local.
- **Machine-global skills retired (user decision 2026-06-16).** `~/.claude/skills/`
  previously held `hora-app-release` + `hora-launcher-icon`; both removed now that
  hora-core is canonical and apps sync from it (they were a name-collision risk for an
  in-app agent seeing both). `~/.claude/skills/` is now empty. Before deleting, diffed
  them against the canonical versions: the `hora-app-release` global's app-specific
  detail is preserved in Pathivu's `android/CLAUDE.md` + Varisankya's stub; the
  `hora-launcher-icon` global's one durable family-level fact — the launcher face is
  **Baloo 2 Bold** (Manjari rejected) — was folded into the canonical
  `hora-launcher-icon` skill first (the rest was obsolete per-app tuning that the
  method-only skill intentionally omits). Varisankya can now add `hora-app-release` to
  its sync set without the collision.
- **Sync-script line endings (fixed 2026-06-17).** The shared
  `templates/sync-shared-skills/sync_shared_skills.sh` checked out as CRLF on a fresh
  Windows clone (`core.autocrlf=true`), breaking `bash`. Fixed at source: hora-core now
  ships a `.gitattributes` with `*.sh text eol=lf`, and the template README +
  conventions.md tell each adopting app to add the same guard. Pathivu flagged it;
  both apps mirror the guard in their own `.gitattributes`.
- **Watch item — Varisankya launcher-icon constants — RESOLVED (2026-06-18).** The user
  ratified Varisankya's launcher icon as the family gold standard and asked for its
  derivation in hora-core, so `brand/launcher-icon/` now holds the canonical "വരി"
  reference vector + a metrics doc that **records those constants durably** (Vstem 121 @
  600px, R_FRAC 0.2454, aspect 1.80), alongside independently re-measured target metrics
  (stem ≈13% of cap-height, R_FRAC ≈0.25, aspect 1.795). They're no longer trapped only in
  Pathivu's `_tools/`, so the "if `_tools/` is cleaned, they vanish" risk is closed.
- **Notification-icon standard ratified (user decision 2026-06-17).** The user confirmed
  Varisankya's notification-shade icon — a **solid white disc with the app's Malayalam
  initial knocked out as a hollow** (single `evenOdd` path, white-on-transparent, 24×24,
  glyph scale ~0.85) — as the firm family standard. Verified hora-core's generator
  (`brand/notification-icon/gen_notification_icon.py`) reproduces Varisankya's shipped
  `ic_notification.xml` exactly. Already documented in `conventions.md` +
  `brand/notification-icon/`; added a "migrating from the older framed treatment" note.
  Pathivu was the only app still on the deprecated framed/stroked treatment; **it has
  now migrated** (commit `106854d`, beta.25): `പ` extracted as a filled silhouette from
  Nirmala UI, knocked out of the disc at scale 0.85, user signed off on a side-by-side.
  Verified Pathivu's `ic_notification.xml` is now structurally identical to the standard
  (same disc path as Varisankya + filled `evenOdd` knockout, no frame/stroke). The whole
  family (വ + പ) is on the ratified standard; no app outstanding.
- **Launcher-icon method improved (2026-06-17).** Pathivu found the horizontal-only
  weight-restore (`dilate_h`) leaves jagged rectangular "tabs/spikes" on vertical stems
  that survive downsampling as pixel spikes. Fix folded into the `hora-launcher-icon`
  skill (new step 6 + a gotcha): contour-smooth the hi-res master (Gaussian blur +
  re-threshold at 50%) before the per-density downsample — dissolves tabs while preserving
  straight edges and stroke weight. **Relayed to Varisankya** to check വരി at high zoom
  (composed the same way: Baloo + `dilate_h`) and regenerate if it has the same artifact.
- **Migration complete; coordination protocol retired (user decision 2026-06-18).** The
  cross-repo migration is done, so the temporary `.agent-mailbox/` channel and its
  `hora-agent-mailbox` skill were removed, and `.gitignore`/`AGENTS.md` references
  dropped. New model: **each Hora app agent edits hora-core directly** — commits to `main`
  (no PRs) and updates the wiki (`master`) itself, under the standing mandates (no secrets,
  2+-app bar, conventions.md as single source of truth). The earlier entries above mention
  mailbox-mediated coordination ("pinged via the mailbox", "resolved replies") — that is
  accurate *history*; the channel no longer exists. This file is now the only shared
  coordination record. NOTE: the app repos' own `AGENTS.md` (e.g. Varisankya mandate 7,
  Pathivu's handoff doc) may still tell their agents to check `.agent-mailbox/`; each app
  agent should drop that on its own side next time it runs — hora-core does not edit
  sibling repos.
- **Agent repo-scope codified as a skill (user decision 2026-06-26).** The fixed
  per-app write boundary — each app agent may write only to **its own app repo + wiki**
  and **hora-core repo + wiki**, with sibling app repos read-only — is now a first-class
  skill, `.github/skills/hora-agent-scope/SKILL.md`, so every Hora app agent inherits it
  on sync (added to Pathivu's `sync_shared_skills.sh` SKILLS list; Varisankya picks it up
  on its next sync). `AGENTS.md` (§ Working agreements, "Agent scope is fixed per app")
  and the wiki `Home.md` agent-scope table both point at it. Rationale: a misdirected
  push to a sibling can corrupt that app's in-flight version/Play-track state — isolation
  prevents silent interference. This generalizes the long-standing "do not touch sibling
  repos" preference into an actionable MUST/MUST-NOT skill.

## Working preferences

- Each Hora app agent updates hora-core `main` and the wiki (`master`) directly; that is
  the expected workflow now (migration complete — see the protocol-retired entry above).
- Do not touch sibling repos under `C:\Users\Aarsh\Source\` unless explicitly asked.

## Resume checklist

- `git status --short`.
- Read `AGENTS.md` and the matching skill.
- Before adding shared code, confirm 2+ apps need it and record the consumption
  mechanism in `docs/conventions.md`.
- Update this file when durable repo state changes.

  - **Standardization Rollout & Web UI Mapping (2026-06-25):** 
    - Adopted Varisankya's Web UI standardization in Pathivu (synced `web_shared.css`, imported it in `globals.css`, and mapped M3 semantic color tokens). Pushed to `pathivu` main, deploying via Vercel.
    - Centralized remaining byte-identical Android components to `hora-core/shared/android/`: `BiometricAuthManager`, `BaseActivity`, `SelectionBottomSheet`, and the `bottom_sheet_selection.xml` layout. Generalized prompts dynamically using resource strings/theme resolution to keep them generic.
    - Promoted `DragReorderCallback` to `hora-core/shared/android/kotlin/util/DragReorderCallback.kt` and updated the sync templates.
    - Updated Pathivu's local sync scripts and pulled down the generated shared assets (deleting duplicate local helpers like `ReorderHelpers.kt`). Verified compile and unit test suites on Android.
    - Shipped beta release `1.0-beta.41` (versionCode `41`), tagged `v1.0-beta.41`, cut GitHub release, and published to Google Play internal/closed testing tracks.
    - Logged updates in GitHub Discussions (Thread #33).

  - **ConfirmationBottomSheet Rollout & Release (2026-06-25):** 
    - Adopted the promoted `ConfirmationBottomSheet` and its layout resource in Pathivu via `sync_shared_android.sh`.
    - Verified compilation and passing unit tests on both Android and Web.
    - Bumped Pathivu Android app version to `1.0-beta.42` (versionCode `42`).
    - Shipped and tagged `v1.0-beta.42`, cut GitHub release with sideloadable APK, and uploaded to Google Play internal track, then promoted to alpha closed testing track.
    - Logged updates in GitHub Discussions (Thread #33).

  - **AboutBottomSheet Promotion & Release (2026-06-26):**
    - Promoted `AboutBottomSheet` (parameterised `githubUrl` constructor arg) and `bottom_sheet_about.xml` layout (MaterialDivider replacing Space) from Pathivu/Varisankya to hora-core shared library (`9b2bc00`). Added both to `sync_shared_android.sh` template.
    - Synced into Pathivu via `sync_shared_android.sh`; updated `SettingsActivity` to pass `"https://github.com/aarshps/pathivu"` as the URL.
    - Bumped Pathivu Android app version to `1.0-beta.43` (versionCode `43`).
    - Shipped and tagged `v1.0-beta.43`, cut GitHub release with sideloadable APK, and uploaded to Google Play internal track, then promoted to alpha closed testing track.

  - **SwipeHelpers Promotion + Agent-Scope Skill (2026-06-26, Varisankya agent):**
    - Promoted `SwipeHelpers.kt` (`SwipeActionCallback`) to `hora-core/shared/android/kotlin/util/` — Varisankya carried the canonical version after Pathivu's enhancement added **opt-in** long-press drag-reorder (`dragEnabled` flag, NestedScrollView edge auto-scroll, scale anim) on top of the sticky-damped swipe-to-action. Drag defaults off, so swipe-only screens are unaffected. Added to `templates/sync_shared_android.sh` `KT_FILES`, the `shared/android/README.md` table, and the `shared-android-source` skill. Also brought the README/skill component lists current with the other recently-promoted classes (`BaseActivity`, `Selection/Confirmation/AboutBottomSheet`, `DragReorderCallback`, `BiometricAuthManager`).
    - Added `hora-agent-scope` skill (started by Varisankya agent `15642df`, refined by Pathivu agent `196d912`) — fixed per-agent write scope (own app repo+wiki + hora-core repo+wiki; sibling repos read-only). Wired a pointer into `AGENTS.md` working agreements.
    - Varisankya adopted via sync; shipped Android `v3.9-beta.14` (versionCode `71`) — built signed AAB+APK on the dev machine (R8 green), cut the GitHub pre-release with sideloadable APK, and **published to Google Play Open Testing (`beta` track, status `completed`)** via Gradle Play Publisher. Secrets were already on disk (`android/app/play_console_key.json`, `android/varisankya-upload-key`, signing creds in `local.properties`), so no Bitwarden unlock was needed. Web auto-deploys via Vercel on push to `main` (live, HTTP 200). **iOS remains blocked on Apple Developer Program enrollment** (account hold) — no signing cert/TestFlight possible. Next free Varisankya versionCode: `72`.

  - **Pathivu FAB fix + branding, then agent-scope release (2026-06-26, Pathivu agent):**
    - Shipped Pathivu `1.0-beta.44` (versionCode `44`): (1) fixed the home FAB collapsing without animation — the AppBar `addOnOffsetChangedListener` was calling `extend()` on every scroll event (verticalOffset is always 0; the toolbar has no scrollFlags), cancelling the in-progress `shrink()`; removed `extend()` from the offset listener and added a `scrollY == 0` re-extend branch to the NestedScrollView listener. (2) "Pathivu" branding — replaced every user-visible "habit/habits" with "Pathivu/Pathivus" across Android (layouts + Kotlin), iOS (Swift), and web (TSX); internal identifiers/analytics unchanged. Tagged `v1.0-beta.44`, GitHub pre-release with sideloadable APK, Play internal + promoted alpha.
    - Shipped Pathivu `1.0-beta.45` (versionCode `45`) — **maintenance, APK byte-identical to beta.44**. Marks the version for the agent-scope governance: adopted the `hora-agent-scope` skill into Pathivu's `sync_shared_skills.sh` and synced an updated `hora-agent-discussions` skill (signature-footer format); brought `android/CLAUDE.md`'s release log current (consolidated vc40–44 + vc45). Tagged `v1.0-beta.45`, GitHub pre-release, Play internal + promoted alpha; web auto-deploys via Vercel on push. **Next free Pathivu versionCode: `46`.**
    - Shipped Pathivu `1.0-beta.46` (versionCode `46`) — **day-rollover review reliability fix, all three platforms.** The "wrap up yesterday" sheet (`DayReviewBottomSheet`) sometimes never appeared on a new day. Root cause: the trigger was driven solely by the `isLoading` StateFlow's `false` transition, which emits only once — on the first Firestore snapshot. With offline persistence (`persistentLocalCache` is enabled on Android, iOS **and** web) that first snapshot is the local cache, which can be empty/stale (fresh install, evicted cache, an unresolved `serverTimestamp` `createdAt`); evaluating against it set `reviewable = false` yet still committed `dayReviewChecked` + `lastActiveDay = today`, suppressing the review for the rest of the day, and the later server snapshot never re-triggered it (a StateFlow doesn't re-emit an unchanged value). Fix: drive the check from the per-snapshot habits data and bail before committing the once-per-launch chance until a non-empty snapshot has loaded — Android (`MainActivity` habits collector), iOS (`MainView` adds `.onChange(of: vm.habits.isEmpty)` + empty guard), web (`page.tsx` gates on a stable `hasHabits` boolean, not the snapshot-identity `habits` array which would cancel the 500 ms timer). The locked `isReviewable`/`isReviewableOn` predicate is unchanged (still vectored by `web/lib/__tests__/dayReview.test.ts`; 42/42 green, web build clean). iOS ships via `ios-build.yml` CI (not compiled on the Windows dev box); `project.yml` version left at `1.0`/`1` as in every prior beta. Tagged `v1.0-beta.46`, GitHub pre-release with sideloadable APK, Play internal + promoted alpha; web auto-deploys via Vercel on push. **Next free Pathivu versionCode: `47`.**

  - **Web shared layer grown to components + Varisankya re-converged (2026-06-27, Varisankya agent).** The web shared layer was CSS-only in the agent-resume history but had already grown to four components (`ServiceWorker`, `Sheet`, `controls`, `SignIn`) consumed by Pathivu; **Varisankya had drifted** (controls in `ui/`, its own `Modal` instead of `Sheet`, stale `ServiceWorker`/`SignIn`/`web_shared.css`, a CSS-only sync script with no manifest). This pass (a) promoted two more byte-shareable M3 primitives from Varisankya into `shared/web/components/`: **`ConfirmDialog`** (Cancel/confirm `Sheet`, `danger`+`busy`) and **`AboutSheet`** (prop-driven app identity + description + optional legal links), (b) upgraded the **family template** `templates/sync_shared_web.sh` from CSS-only to the component-syncing form (FILES map of all six shared files + manifest + `__HORA_APP_NAME__` rewrite), (c) **re-converged Varisankya web** onto the shared layer (top-level `components/`, dropped its local `Modal`/`controls`/`ConfirmDialog`/`AboutDialog`, prop-driven `SignIn` wired in `page.tsx`, manifest added), and (d) updated the README table + `conventions.md` "Shared Web source" to the six-file set. The two new components are promoted to hora-core and **ready for sibling apps to adopt** — Pathivu (still on raw browser `confirm()`/`alert()` in its settings, with no About dialog) is the obvious next adopter; this pass touched **no sibling repo**, with Varisankya as the reference consumer. Varisankya web builds clean and passes its vitest suite. The shared web component set is now `ServiceWorker`, `Sheet`, `controls`, `SignIn`, `ConfirmDialog`, `AboutSheet`.

  - **Web shared layer: settings primitives + EmptyState promoted (2026-06-27, Varisankya agent).** Continued the web standardization, next batch. Promoted the **Settings design language** as `shared/web/components/settings.tsx` (`SettingsSection`, `SettingsSectionLabel`, `SettingsRow`, `SettingsToggle`, `SettingsDivider`, `SettingsLinkRow`) and a prop-driven **`EmptyState`** — both were reimplemented near-identically in Varisankya and Pathivu (each had local `Card`/`Row`/`Divider`(+`SectionLabel`/`ToggleRow`) settings helpers and an `EmptyState`), now single-sourced. Canonical preserves Varisankya's look. Added both to the sync template + Varisankya's FILES; Varisankya synced and refactored its `SettingsView` (dropped local `Card`/`SectionLabel`/`Row`/`Divider`) and `App.tsx` empty-state onto them. **Pathivu untouched this pass** — it can adopt on its next sync, dropping its local equivalents. README + `conventions.md` updated. The shared web component set is now `ServiceWorker`, `Sheet`, `controls`, `SignIn`, `ConfirmDialog`, `AboutSheet`, `settings`, `EmptyState`. Varisankya web builds clean + 41/41 vitest pass. **Still app-local (legitimately divergent / not yet 2-app):** theme-toggle plumbing, the loading skeleton vs spinner, and per-app screens.

  - **Web shared layer: ScreenHeader promoted (2026-06-27, Varisankya agent).** Continued the campaign: promoted `shared/web/components/ScreenHeader.tsx` — the sticky secondary-screen top app-bar (back button + title + optional `trailing` slot, `centered` option, `onBack` callback; pure React, no `next/link` coupling). Both apps repeat this pattern verbatim within themselves (Varisankya: `SettingsView` + `HistoryView`; Pathivu: `settings` + `stats`); cross-app variation in alignment/routing is handled by props. Varisankya adopted it in `SettingsView` + `HistoryView` (dropped the duplicated `<header>` blocks + now-unused `ArrowLeft` imports). Pathivu can adopt on its next sync (swap its `<Link href>` for `onBack={() => router.push("/")}` + `centered`). Template/README/conventions updated. Shared web set is now `ServiceWorker`, `Sheet`, `controls`, `SignIn`, `ConfirmDialog`, `AboutSheet`, `settings`, `EmptyState`, `ScreenHeader`. Varisankya web builds clean + 41/41 vitest pass. **Rollout:** web auto-deploys via Vercel on push; this batch is **web-only** (no Android/iOS source changed since `v3.9-beta.14`/vc71), so no native beta was warranted this pass; iOS remains blocked on Apple enrollment.

  - **Incident: Android "logged out, can't sign back in" — config-side, NOT the web work (2026-06-27, Varisankya agent).** User got logged out of the Varisankya Android app and couldn't sign back in, suspecting the web-standardization campaign caused a regression. **It did not** — the web work is `web/`-only and cannot touch Android auth; the Android binary was unchanged since `v3.9-beta.14`/vc71, the sign-in code is correct (`setFilterByAuthorizedAccounts(false)`), and an Identity-Toolkit liveness probe confirmed the Firebase Auth API key + authorized domains are healthy. The failure is **server/config-side** (Firebase rejects the Google ID token): prime suspects are the Google provider disabled, the OAuth **web client** (`default_web_client_id`) no longer matching the project's Google-provider config, **App Check** enforcement, or the Google Cloud **OAuth consent screen** still in "Testing" (7-day refresh-token expiry). The app **hid** it — `firebaseAuthWithGoogle`'s failure branch called `updateUI(false)` silently. **Fix shipped (Varisankya v3.9-beta.15/vc72, Play Open Testing):** surface the real Firebase failure reason (log + Snackbar) + add a `GetSignInWithGoogleOption` fallback on `NoCredentialException` so a signed-out user gets the full account picker + consent. **Lesson for siblings (Pathivu, future):** both family apps use the same Firebase + Credential Manager Google sign-in — verify your own credential/`signInWithCredential` failure branches *surface* the reason (never swallow them), and treat "suddenly logged out + can't sign back in" as a Firebase/Google Cloud **config** issue first, not an app or web regression. (Varisankya wiki → Troubleshooting → "Sign-in / Auth" has the on-screen-error → config-fix table.)

  - **Web shared layer: M3E haptics factory promoted (2026-06-27, Varisankya agent).** Promoted `shared/web/lib/haptics-core.ts` — the **first shared web *lib*** (vs a component): `createHaptics(isEnabled)` returns the M3E `{tick,click,success,warning,error}` vibration vocabulary, matching the native Android `PreferenceHelper` + iOS `Haptics.swift` schemes. The "haptics enabled" pref is **injected** because the two apps store it under different keys (`haptics_enabled` vs `pathivu-haptics`), so the shared file stays app-key-free; each app wires it in a one-line local `lib/haptics.ts` (`createHaptics(() => <its pref>)`). This establishes the `shared/web/lib/` location + the **injected-dependency (factory) pattern** for shared web utils (documented in README/conventions). Varisankya adopted it: synced `lib/haptics-core.ts`, added the wiring, migrated its 6 `haptic()` call sites to `haptics.click()` (behaviour-preserving — its old `haptic()` was `vibrate(10)` = `click`), and removed the old `haptic()` from `lib/prefs.ts`. Pathivu (already on the named scheme, 14 call sites) can adopt by syncing the core + reducing its `lib/haptics.ts` to the wiring. Shared web set: 9 components + `lib/haptics-core.ts`. Varisankya web builds clean + 41/41 vitest pass. **The clean verbatim-shareable web surface is now essentially exhausted** — remaining UI is business-specific or legitimately divergent (theme-toggle plumbing, loading skeleton vs spinner, per-app home headers/screens).

  - **Web design-language convergence — iteration 1 (2026-06-27, Varisankya agent; user-directed).** The user flagged (side-by-side screenshots) that the Varisankya + Pathivu *web* home screens don't read as one family and asked to converge them toward a shared Hora web design language — Varisankya now, Pathivu's agent to align to the **same hora-core spec** next (multi-iteration). **User decisions this iteration:** (1) **neutral surfaces + per-app accent** (NOT a unified palette — each app keeps its brand colour; only surfaces are held neutral), (2) **centered** home app-bar title, (3) **extended** (icon+label) FAB. Done for Varisankya: (a) **palette neutralized** — `scripts/gen-theme.mjs` now draws accent roles (primary/secondary/tertiary/error) from `SchemeTonalSpot` (vivid teal) but surface/background/outline/neutral roles from `SchemeNeutral` (~0 chroma), so surfaces are clean neutral dark (`#121414`/`#1f2020`) instead of green-tinted while the teal accent (`#80d4d6`) stays; regenerated `app/theme.css`. (b) Promoted **`AppBar`** (centered home top-bar: leading/title/actions) + **`Fab`** (extended) to `shared/web/components/` and adopted them in Varisankya `App.tsx`. README/conventions/template updated; the design-language spec is on the hora-core wiki (Shared-Web → "Family look"). **Stays per-app:** the brand accent hue (teal vs lavender — intentional identity) + business content (rows/hero). Shared web set: 11 components + 1 lib. Varisankya web builds clean + 41/41 vitest pass. **Pathivu agent next:** adopt `AppBar` + `Fab` (its circular FAB → extended) — its surfaces are already neutral — to land the same family look.

  - **Web design-language convergence — iteration 2: grouped-list standard (2026-06-28, Varisankya agent; user-directed).** User chose the **grouped-continuous list** (Varisankya's existing `.item-*` pattern) as the family standard for how list items are carded — over Pathivu's separate floating cards. Since Varisankya already complies, this iteration **ratifies** the standard: added a `.grouped-list` container utility to `shared/web/res/css/web_shared.css` (a tight 2px-gap column; pairs with the existing `.item-single/first/middle/last` shape classes the app assigns per item) so the full grouped-list pattern is one named, drift-proof standard. Varisankya adopted it (`SubscriptionList`'s `<ul>` → `.grouped-list`). Documented as family-look **rule #4** (the four rules: neutral surfaces + per-app accent, centered `AppBar`, extended `Fab`, **grouped lists**) on the Shared-Web wiki + README/conventions. Row **content** + the per-row complete button stay per-app — the check's prominence legitimately differs (primary action in Pathivu, secondary convenience in Varisankya). Varisankya web builds clean + 41/41 vitest pass. **Pathivu agent next:** converge its separate habit cards to `.grouped-list` + `.item-*` (computing single/first/middle/last per row).

  - **Web design language — uniform palette standardized in hora-core (2026-06-28, Varisankya agent; user-directed).** The family web colour rule shifted (user decision, committed earlier this pass) from "neutral surfaces + per-app accent" to **"neutral surfaces + uniform accents"**: a clean monochrome neutral surface scale + a single brand-neutral indigo/periwinkle accent for the **whole family** (no per-app brand hue — Varisankya web gave up its teal). Varisankya's web had already shipped these exact values (matching Pathivu: `#121212`/`#212121` surfaces + `#aec6ff` dark primary). This pass closed the gap the user flagged — **the palette values lived only in Varisankya's local `gen-theme.mjs`, not in hora-core**: promoted them to **`shared/web/res/theme-palette.mjs`** (`LIGHT`/`DARK` `--md-*` maps) as the canonical family standard, added to the web sync (`→ web/scripts/theme-palette.mjs`), and refactored Varisankya's `gen-theme.mjs` to **import** the synced canonical values instead of hard-coding them. `theme.css` regenerated **byte-identical** (no visual change — the colours were already live). README + conventions + Shared-Web wiki rule 1 now point at the canonical palette. **Per-app toggle plumbing stays local** (Varisankya `data-theme` attribute, Pathivu `.dark` class) — only the values are shared. Build clean + 41/41 vitest. **Pathivu agent next:** align its hand-authored `theme.css` values to `theme-palette.mjs` (they already match) so the source of truth is hora-core for it too.

  - **iOS shared-source layer established (2026-06-26, Pathivu agent).** Until now only Android (`shared/android/`, 59 files) and web (`shared/web/res/css/web_shared.css`) had a shared layer; **iOS had none**. Audited Pathivu's iOS Swift against Varisankya (read-only reference) by app-name-normalized diff and promoted the three byte-identical components to **`shared/ios/swift/`** (hora-core `c389d3d`): `Haptics.swift` (M3E haptic helper, verbatim), `BiometricAuth.swift` (LocalAuthentication App-Lock wrapper; default unlock reason uses a `__HORA_APP_NAME__` token), and `SelectionSheet.swift` (glass single-choice picker — the SwiftUI counterpart of the already-shared Android `SelectionBottomSheet`, verbatim). Added `templates/sync_shared_ios.sh` (mirrors the Android/web sync: file→dest map, token substitution, provenance manifest), `shared/ios/README.md`, and documented the layer in `conventions.md` (new "Shared iOS source" section) + the `hora-repo-map` skill + wiki `Home.md`. **Pathivu adopted** via `ios/tools/sync_shared_ios.sh` (Pathivu `40be110`) — no behaviour change (generated Swift is functionally identical to the prior hand-maintained copies; only a do-not-hand-edit header added). Not compiled on the Windows box; `ios-build.yml` CI validates. **Varisankya can adopt the same three on its next pass** (it carries the canonical-equivalent originals today). Further iOS candidates identified but deferred (more app-specific): `NotificationDelegate` (~10 diff), `SignInView` (~14), `AuthService` (~40).



  - **New sibling app Muthal created end-to-end (2026-07-01, Muthal agent).** Added the family's third app — **Muthal** (Malayalam മുതൽ, "capital/principal"), a minimal income & expense ledger for institutions (temples/churches/libraries). Cross-platform monorepo `aarshps/muthal` built to hora-core standards: `shared/domain` (SPEC + golden-vectors: multi-institution model, entry dual-write to a flat mirror, UTC month bucketing, currency/summary/categories), `shared/firebase` (per-user rules + `entries` collection-group read), **web** (Next.js static-export PWA on Firebase Hosting — **live at https://hora-muthal.web.app**, consumes the shared web design system via the sync script), **android** (Kotlin/AGP9/Material3/ViewBinding, Credential Manager, dual-write repo — `assembleDebug`+`testDebugUnitTest`+signed `bundleRelease` all green), **iOS** (SwiftUI/XcodeGen, authored + CI). All three assert the same `golden-vectors.json`. Dedicated Firebase project **`hora-muthal`** (Firestore+rules deployed, Google provider enabled, 3 apps registered). Icons generated from the shared Baloo Chettan 2 engine — **added a `muthal` entry (wordmark മുത) to `brand/launcher-icon/gen_launcher_icon.py`**. Secrets vaulted in Bitwarden item `Muthal` (folder Hora). **Beta status:** web live; Android GitHub release `v1.0-beta.1` (signed APK) shipped, Play internal pending the one-time app-record + service-account; **iOS TestFlight blocked family-wide on Apple Developer enrolment** (same hold as Varisankya). No sibling repo was modified; only hora-core (this entry + README family table + the icon-engine `APPS` addition) and the Muthal repo/wiki.

  - **Icon sizing standard: the "max-in-circle" rule (2026-07, Muthal agent; user-directed).** The owner set a precise geometric rule for **all** family icons: the wordmark is scaled so its *circumscribing circle* (smallest circle centred on the canvas containing the wordmark's bounding box) is the **largest circle that fits the icon's usable area** — i.e. the wordmark is the max size that fits inside that centred circle. Replaced the ad-hoc per-variant `r_frac` values in `brand/launcher-icon/gen_launcher_icon.py` with three context constants: **`FULL_RFRAC=0.5`** (unmasked/circular: Play 512, iOS AppIcon, web favicon + PWA "any", legacy + round launcher — largest circle in the square canvas), **`FG_RFRAC=0.305`** (Android adaptive foreground + monochrome — the 66dp/108dp adaptive safe circle), **`MASK_RFRAC=0.40`** (maskable web icon — W3C 80% safe circle). Documented in `docs/conventions.md` (App icons), `brand/launcher-icon/README.md`, and the `hora-launcher-icon` skill. **Regenerated Muthal's full icon set** to the new sizes (web/iOS/Play now fill 0.86×0.51 of canvas vs the old ~0.52×0.30 flat / 0.71×0.42 play). **Siblings (Pathivu, Varisankya) not regenerated** — their committed icons keep the old sizing until their own agents re-run `python gen_launcher_icon.py <app>` (the engine change is picked up automatically on next regen). Prior ad-hoc constants (`R_FRAC=0.2435`, `PLAY_RFRAC=0.41`, flat 0.30) are superseded.

  - **Muthal 1.0-beta.2 released & deployed (2026-07-02, Muthal agent):**
    - Bumped Android `versionCode = 2` and `versionName = "1.0-beta.2"` in `android/app/build.gradle.kts`.
    - Compiled fresh, signed release AAB + APK (`app-release.aab` and `app-release.apk`) including the new `max-in-circle` sizing standard icons.
    - Deployed the web app's static export to Firebase Hosting.
    - Used the `browser` subagent to upload `app-release.aab` to Google Play Console's internal testing track, retrieve the Play App-Signing SHA-256 fingerprint (`D0:53:78...4A`), and register the fingerprint in the Firebase project (`hora-muthal`) settings so Google Sign-In works for testers.
    - Updated `CLAUDE.md` and wiki `Build-and-Release.md`. Tagged the release as `v1.0-beta.2` in Git.

  - **Tester recruitment & Google Group standards (2026-07-02, Muthal agent):**
    - Documented `<app>-testers@googlegroups.com` Google Group naming pattern, privacy standards, and welcome message template as a family standard in `docs/conventions.md` and `hora-core.wiki` (`Home.md`).
    - Redeployed Muthal web on Vercel (`muthal-web.vercel.app`) to pick up the regenerated `max-in-circle` icons (verified HTTP 200 on `/icon.png`).

  - **Muthal 1.0-beta.3 — device-test fixes + two family standards corrected (2026-07-02, Muthal agent).** The owner's first on-device Internal Testing run surfaced four issues; all addressed end-to-end:
    1. **Package name / placeholder icon on the Play install page** — *expected pre-review behaviour* ("Temporary app name 'com.hora.muthal (unreviewed)'"): the store listing (name + graphics) was only sent with the first review submission; resolves when Google approves it. No action.
    2. **App rendered Roboto, not the brand font** — Muthal's Android app had **never run `sync_shared_android.sh`** (no `res/font/`, no `type.xml`, bare theme). Fixed: full shared sync + `Theme.Muthal` typography wiring + the two app-local glue objects. **Conventions doc corrected:** the shared-android consumption note claimed only `Constants` was needed — it now documents that an app must provide **`Constants` AND `PreferenceHelper`** in its base package, and must wire `fontFamily` + all fifteen `textAppearance*` attrs in its own `themes.xml` (syncing files alone changes no rendered text).
    3. **"Sign-in cancelled" on device** — root cause: Firebase had **only the Play App-Signing SHA-256**; Google Sign-In requires **SHA-1**, and Play-installed builds are signed by the *Play* key, not the upload key. Registered Play SHA-1 + upload SHA-1 (console-side, no rebuild). **New conventions section:** "Google Sign-In on Android — SHA fingerprints" (register BOTH certs' SHA-1s; only `GetCredentialCancellationException` may be reported as "cancelled" — Muthal's catch-all was masking the misconfiguration, same lesson as Varisankya's 2026-06-27 incident).
    4. **Shipped `1.0-beta.3` (vc 3)** to Play internal testing via gpp `publishReleaseBundle` + GitHub release `v1.0-beta.3`.
    - **DR gap closed:** the Play service-account key was documented as vaulted but **absent from the Muthal Bitwarden item** (`retrieve_secrets.sh` silently wrote a 0-byte file). Restored the account-level key from a sibling item, stored it on the Muthal item (two-part base64 fields), and hardened `retrieve_secrets.sh` to fail loudly on missing/empty vault fields — siblings should adopt the same guard.
    - **Icon sizing standard REVERTED to per-surface values (user-directed):** the owner rejected the 2026-07 "max-in-circle full-bleed" look on the Play 512 ("writing should be max sized within the same circle as Pathivu"). Measured the siblings' shipped assets and restored those values as the canonical constants in `gen_launcher_icon.py`: **PLAY 0.41, FLAT (iOS + web "any") 0.30, LAUNCHER 0.343, FG/monochrome 0.246, MASK 0.24**. `FULL_RFRAC=0.5` is gone; conventions.md rewritten (per-surface table + rationale). Muthal's full icon set regenerated to match siblings within ~1px; **siblings are already on these values** — no regen needed there.
    - **New standard: marketing/static-image typography** — any English text baked into a static image (Play feature graphic, banners) uses the real **Google Sans Flex variable font at 'ROND' 100** (the file in `shared/android/res/font/`), NOT the Nunito web approximation or a system font. Documented in conventions.md; Muthal's feature graphic regenerated with it.
    - Also this session: Muthal web sign-in fixed end-to-end on Vercel (authorized domain + OAuth redirect URIs + 3 missing `NEXT_PUBLIC_FIREBASE_*` prod env vars), Play app-content declarations completed (incl. the **advertising ID declaration** — required for Android 13+ targets; Firebase Analytics merges `AD_ID` into the manifest, so declare *Yes → Analytics*), and the Closed Testing - Alpha submission (13 changes) genuinely sent for review.
