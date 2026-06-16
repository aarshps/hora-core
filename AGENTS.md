# AI Agents Context — hora-core

Authoritative context for AI agents (Claude Code, Gemini CLI, Codex, etc.) working in
this repo. `hora-core` holds items shared **across** the Hora app family (Varisankya,
Pathivu, future siblings) — not items that belong to a single app.

Keep this file current when conventions change. Do **not** add per-session activity
logs — git history is the record. Durable state and handoff notes go in
`docs/agent-resume.md`.

---

## Purpose & scope

- Shared brand/design, cross-app conventions, shared agent skills, reusable tooling.
- If something is specific to one app, it belongs in that app's repo, not here.
- Before adding code, confirm at least two family apps actually need it.

## Core mandates

1. **Security is the top priority.** Never commit secrets, keys, tokens,
   service-account JSON, or `google-services.json`. Because this repo is **public**,
   treat everything committed as world-readable forever. Before any push, scan for
   private-key patterns (`BEGIN.*PRIVATE KEY`), Firebase keys (`AIza`), and OAuth
   secrets (`GOCSPX-`).
2. **Public repo.** `hora-core` is public. Do not move app-private material here.
3. **Single source of truth.** Shared conventions live in `docs/conventions.md`. When
   a convention changes, update that file in the same change — do not let apps drift.

## GitHub identity

- This repo uses the GitHub account **`aarshps`**. On this Windows machine, plain `gh`
  is already authenticated as `aarshps` (keyring) — use it directly.
- The older Mac-only `scripts/gh-aarshps` wrapper and `/Users/aps/...` profile path do
  **not** exist here; ignore any historical references to them.
- Verify with `gh api user --jq .login` if account identity matters.
- Do not change global `gh`/git auth state. Keep changes scoped to this repo.

## Working agreements

- The user manages this repo directly on `main`; pushing to `main` is expected when
  asked. The wiki's default branch is `master`.
- Do not modify sibling repos under `C:\Users\Aarsh\Source\` unless explicitly asked.
- Repo-local skills live under `.github/skills/<name>/SKILL.md`. Open only the skills
  relevant to the task. Keep each `SKILL.md` ≤ 100 lines, one narrow job each.
- Read `docs/agent-resume.md` before resuming paused work.
