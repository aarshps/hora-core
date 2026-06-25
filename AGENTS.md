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

- **Any Hora-family app agent may edit this repo directly.** The migration that needed a
  coordination layer is complete — Pathivu, Varisankya, and future sibling agents commit
  straight to `main` (no PRs) and update the wiki (default branch `master`) themselves.
  The core mandates above bind every such change: no secrets, the 2+-app inclusion bar,
  and `docs/conventions.md` stays the single source of truth.
- **`main` and the wiki (`master`) move together — end to end, in the same pass.** Whenever a change
  you push to `main` alters something the wiki describes (a shared component added / removed / renamed,
  a new standard or convention, a brand or engine change, an area's purpose), reflect it in the wiki
  (`master`) **before you call the task done** — never leave the wiki lagging `main`. The wiki is the
  human-facing summary of this repo, so updating it is part of "done", exactly like keeping
  `docs/conventions.md` current. (A pure internal refactor that changes nothing the wiki states needs
  no wiki edit — but verify that before skipping it.) This binds every app agent (Pathivu, Varisankya,
  future siblings) equally.
- **No transient/transactional updates in the main repository.** Progress tracking, live testing countdowns, current tester numbers, active progress metrics, and other transient status tracking belong strictly in the wiki repository (`master`). The main repository (`main`) must only contain static documentation, configurations, stable milestone releases, and architectural specs.
- **GitHub Discussions for Coordination:** Any updates, progress changes, or releases must be posted in the [GitHub Discussions forum of hora-core](https://github.com/aarshps/hora-core/discussions). Agents must read recent discussion threads at the start of each session and post their own session updates/status when closing to ensure family-wide alignment. All posts and comments in the discussions forum must explicitly state the agent's identity, unique session conversation ID, and host work environment (e.g., 'Pathivu Agent (<unique-id>), working from Beeyeswon').



- There is **no agent-to-agent coordination protocol** anymore. The former local
  `.agent-mailbox/` channel was retired once migration finished; coordinate by editing
  this repo's committed docs directly. `docs/agent-resume.md` is the durable record of
  cross-app decisions — read it before resuming paused work and append to it when you
  make a decision that outlives your session.
- Do not modify sibling repos under `C:\Users\Aarsh\Source\` unless explicitly asked.
- Repo-local skills live under `.github/skills/<name>/SKILL.md`. Open only the skills
  relevant to the task. Keep each `SKILL.md` ≤ 100 lines, one narrow job each.
