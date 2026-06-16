---
name: hora-repo-map
description: Use for a fast map of hora-core to decide where shared-across-the-family work belongs (brand, conventions, agent skills) versus an individual app's repo.
---

# Hora-core Repo Map

`hora-core` holds items shared **across** the Hora app family. Use this skill to pick
the right area before editing.

## Areas

- `brand/` — shared visual identity (Material 3 tokens, Malayalam launcher-icon
  conventions, family logos). Start with `brand/README.md`.
- `docs/conventions.md` — the shared stack and conventions every app follows. Edit here
  when a family-wide convention changes.
- `docs/agent-resume.md` — durable repo state and handoff notes.
- `.github/skills/` — agent skills shared across the family.
- `AGENTS.md` — cross-cutting agent context and the security/identity mandates.

## Routing hints

- Visual/brand work shared by 2+ apps → `brand/`.
- A rule every app must follow → `docs/conventions.md`.
- Anything specific to **one** app → that app's own repo, **not** here.
- Repo workflow, GitHub identity, or handoff context → `AGENTS.md` / `.github/skills/`
  / `docs/agent-resume.md`.

## Guardrails

- This repo is **public**: never add secrets, keys, or `google-services.json`.
- Before adding shared **code**, confirm 2+ apps need it and record the consumption
  mechanism in `docs/conventions.md`.
