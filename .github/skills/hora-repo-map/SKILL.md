---
name: hora-repo-map
description: Use for a fast map of hora-core to decide where shared-across-the-family work belongs (brand, conventions, agent skills) versus an individual app's repo.
---

# Hora-core Repo Map

`hora-core` holds items shared **across** the Hora app family. Use this skill to pick
the right area before editing.

## Areas

- `brand/` — shared visual identity (Material 3 tokens, family logos, and the unified
  Baloo Chettan 2 icon engine `launcher-icon/gen_launcher_icon.py` that generates every
  brand mark on every surface — Android launcher/adaptive/monochrome/legacy/round +
  notification, iOS, web favicon/PWA, Play icon + feature graphic, web OG/social image,
  GitHub repo social preview — from one spec; STRICT, no hand-authored exceptions, see
  `conventions.md` → "Brand mark standard"). Start with `brand/README.md`.
- `shared/android/` — canonical Android **source** shared verbatim across apps (dimens /
  type / chip-color resources + `ChipHelper`/`ThemeHelper`/`AnimationHelper.kt`). Synced
  into each app via `templates/sync_shared_android.sh`; the `shared-android-source` skill
  has the detail.
- `shared/ios/swift/` — canonical **Swift** shared verbatim (modulo one display-name token)
  across apps (`Haptics`, `BiometricAuth`, `SelectionSheet`). Synced via
  `templates/sync_shared_ios.sh`; see `shared/ios/README.md`.
- `shared/web/res/css/` — canonical **Web** stylesheet (`web_shared.css`: M3 tokens, shapes,
  shared component classes). Synced via `templates/sync_shared_web.sh`.
- `templates/` — copy-and-customize starting points for a new app's `shared/`
  contract folder (e.g. `shared-firebase/`) plus the per-app sync scripts. Not a runtime
  dependency.
- `docs/conventions.md` — the shared stack and conventions every app follows. Edit here
  when a family-wide convention changes.
- `docs/agent-resume.md` — durable repo state and handoff notes.
- `.github/skills/` — agent skills shared across the family.
- `AGENTS.md` — cross-cutting agent context and the security/identity mandates.

## Routing hints

- Visual/brand work shared by 2+ apps → `brand/`.
- A boilerplate file a new app would otherwise paste from a sibling → `templates/`.
- An Android resource/Kotlin file used byte-identically by 2+ apps → `shared/android/`
  (synced via its script, not hand-pasted).
- A rule every app must follow → `docs/conventions.md`.
- Anything specific to **one** app → that app's own repo, **not** here.
- Repo workflow, GitHub identity, or handoff context → `AGENTS.md` / `.github/skills/`
  / `docs/agent-resume.md`.

## Guardrails

- This repo is **public**: never add secrets, keys, or `google-services.json`.
- Before adding shared **code**, confirm 2+ apps need it and record the consumption
  mechanism in `docs/conventions.md`.
