---
name: hora-repo-map
description: Use when you need a fast map of the Hora repo to decide whether work belongs in the Angular app, ASP.NET service, Flyway migrations, or GitHub/security docs.
---

# Hora Repo Map

Use this skill when you need to choose the correct area of the repo before editing.

## Main Areas

- `Hora.App/hora`: Angular frontend. Start with `package.json`, `src/main.ts`, and `src/app/`.
- `Hora.Sv/Hora/Hora.Web`: ASP.NET Core web app. Start with `Program.cs`, `Startup.cs`, and `Controllers/`.
- `Hora.Sv/Hora/Hora.Db.Ef`: EF entities, DbContext, and repositories used by the service.
- `Hora.Db/Hora.Flyway`: database migrations and Flyway CLI packaging. Start with `conf/flyway.conf` and `sql/`.
- `.github/workflows`: security and dependency automation.

## Routing Hints

- UI behavior or browser dependency work usually belongs under `Hora.App/hora`.
- API behavior, DI wiring, and HTTP endpoints usually belong under `Hora.Sv/Hora/Hora.Web`.
- Schema or seed changes belong under `Hora.Db/Hora.Flyway/sql`.
- Repo workflow, GitHub account, or handoff context belongs in `AGENTS.md`, `.github/skills/`, or `docs/agent-resume.md`.
