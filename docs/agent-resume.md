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
  - **Open for the app agents** (adoption owned per app, not done from here): sync
    `settings-page-standards` + `shared/android/` source per app. *(Icon-engine adoption is
    now done for both apps — Pathivu beta.35, Varisankya beta.8; see the 2026-06-23 entry.)*

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
  unused long-press app shortcuts). **Pathivu still has the duplicated copies** — it adopts
  on its next pass (sync + trim, same as Varisankya). This closes the staged follow-up.

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
