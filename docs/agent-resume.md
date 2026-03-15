# Agent Resume

## Start Here

- Read `AGENTS.md`.
- Open only the relevant skill files in `.github/skills/`.
- If the task touches GitHub, use `./scripts/gh-aarshps ...` and verify the login resolves to `aarshps`.

## Repo Map

- `Hora.App/hora`: Angular frontend.
- `Hora.Sv/Hora/Hora.Web`: ASP.NET Core web app.
- `Hora.Sv/Hora/Hora.Db.Ef`: EF entities and repositories.
- `Hora.Db/Hora.Flyway`: Flyway config and SQL migrations.
- `.github/workflows`: security and dependency automation.

## Durable Repo State As Of 2026-03-15

- GitHub CLI and GitHub-authenticated git operations in this repo are scoped to the `aarshps` workspace profile.
- `scripts/gh-aarshps` points at `/Users/aps/Source/aarshps/.gh-aarshps`; plain `gh` must not be used from this repo.
- `Hora.Db/Hora.Flyway/conf/flyway.conf` contains placeholders only. The previously committed DB secret was removed and rotated.
- Frontend dependencies were manually remediated to mirror-available Angular `21.2.2` and matching lockfile updates.
- Security overrides currently live in `Hora.App/hora/package.json`.
- Stale Dependabot PRs tied to the prior security cleanup were closed after the manual fix landed.
- Stale `aarshps/hora` notification threads were marked read.

## Working Preferences Recorded On 2026-03-15

- Do not run, build, or test this app on this machine unless the user explicitly asks in the current task.
- When you dismiss alerts or close shared GitHub threads, leave a short rationale.

## Resume Checklist

- Run `git status --short`.
- Read the matching skill and the relevant module doc.
- If dependency work is involved, compare `Hora.App/hora/package.json` and `Hora.App/hora/package-lock.json` together.
- If DB work is involved, keep credentials local and out of git.
- Update `docs/agent-resume.md` when durable repo state changes.
