---
name: hora-security-workflow
description: Use for secret handling, Dependabot triage, security alert cleanup, Flyway config changes, and frontend dependency remediation in this repo.
---

# Hora Security Workflow

Use this skill when the task touches secrets, alerts, dependency PRs, or security-sensitive config.

## Rules

- Never commit real credentials. Keep `Hora.Db/Hora.Flyway/conf/flyway.conf` placeholder-only in git.
- If a secret was exposed, remove it from source, note the rotation requirement, and avoid repeating the value anywhere else.
- Update `Hora.App/hora/package.json` and `Hora.App/hora/package-lock.json` together for JS dependency changes.
- Prefer versions that are actually available from the repo's package mirror instead of assuming upstream releases can be installed here.

## Workflow

1. Inspect active alerts or PRs with `./scripts/gh-aarshps ...` before changing code.
2. Prefer a direct code or dependency fix over blindly merging stale security PRs.
3. Record exact rationale when dismissing alerts or closing superseded PRs.
4. Recheck alert and PR state after the fix so the repo is left in a clean security state.

## Touchpoints

- `Hora.Db/Hora.Flyway/conf/flyway.conf`
- `Hora.App/hora/package.json`
- `Hora.App/hora/package-lock.json`
- `.github/workflows/`
- `docs/agent-resume.md`
