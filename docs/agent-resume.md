# Agent Resume — hora-core

## Start here

- Read `AGENTS.md`, then this file.
- Open only the relevant skill under `.github/skills/`.
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
