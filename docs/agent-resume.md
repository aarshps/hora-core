# Agent Resume — hora-core

## Start here

- Read `AGENTS.md`, then this file.
- Open only the relevant skill under `.github/skills/`.
- Check `.agent-mailbox/` (gitignored, same-machine only) for notes from other
  concurrently-running Hora-family agent sessions — see
  `.github/skills/hora-agent-mailbox/SKILL.md`. It won't exist on a fresh clone.
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
- **Deferred UI-standard skills — partially reopened.** Checked Pathivu's code against
  Varisankya's deferred standards: `m3e-haptic-standards`, `m3e-animation-standards`
  (Pathivu has its own `util/AnimationHelper.kt`), `skeleton-loading-standards`
  (Pathivu has skeleton layouts), and `android-15-standards` (de-versioned — Pathivu is
  on `targetSdk=36` + edge-to-edge) **do** meet the 2+ app bar; Varisankya will
  generalize these four (method-only) into `.github/skills/`. `app-performance-standards`
  stays app-local (no baseline-profile evidence in Pathivu). `m3-dynamic-colors` /
  `app-readiness-policy` remain app-local.
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

## Working preferences

- The user updates `main` and the wiki (`master`) directly; pushing when asked is
  expected.
- Do not touch sibling repos under `C:\Users\Aarsh\Source\` unless explicitly asked.

## Resume checklist

- `git status --short`.
- Read `AGENTS.md` and the matching skill.
- Before adding shared code, confirm 2+ apps need it and record the consumption
  mechanism in `docs/conventions.md`.
- Update this file when durable repo state changes.
