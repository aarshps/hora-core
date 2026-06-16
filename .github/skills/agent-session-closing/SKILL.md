---
name: agent-session-closing
description: Standard operating procedure for concluding an AI agent session in a Hora-family repo, ensuring the workspace is left clean, documented, and resilient for the next agent or human developer.
---

# Agent Session Closing Protocol

Before concluding a session, run through this checklist so the repo is left in a clean,
documented state.

## 1. Documentation & guardrails update
- Review what was accomplished.
- Update `AGENTS.md`/`CLAUDE.md`, `README.md`, and any relevant `SKILL.md` to reflect new
  architectural decisions, environment changes, or newly discovered constraints.
- If a new repeated task emerged, write a new granular skill (keep it short — see
  `agent-skill-standards`) in the repo's own skill directory.

## 2. Workspace cleanup
- Confirm no credentials, keystores, or `.env` values were staged or committed.
- Confirm secret-retrieval scripts (e.g. `retrieve_secrets.sh`) are gitignored and documented.
- Remove temporary debugging files or local test artifacts not meant for version control.

## 3. Final validation
- Run the project's core build command (e.g. `./gradlew assembleDebug` for Android) to confirm it
  still compiles.
- Run available lint/format checks.

## 4. Commit and push
- Stage only the intended files — never a blanket `git add -A` in a repo with secret-bearing
  untracked files nearby.
- Write a clear, concise commit message summarizing the session's impact.
- Push per the repo's own workflow rule — some Hora repos commit straight to `main` with no PRs;
  check the repo's `AGENTS.md`/`CLAUDE.md` before assuming.

## 5. Session summary
Give the user a concise summary: what was accomplished, what docs were updated, and any
recommended next steps.
