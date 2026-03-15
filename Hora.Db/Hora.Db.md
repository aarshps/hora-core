# Hora.Db

- Database migration assets live in `Hora.Db/Hora.Flyway`.
- SQL migrations are in `Hora.Db/Hora.Flyway/sql`.
- Local Flyway configuration lives in `Hora.Db/Hora.Flyway/conf/flyway.conf`.
- `flyway.conf` must stay placeholder-only in git. Inject real JDBC URL, user, and password locally when needed.
- `flyway` and `flyway.cmd` are the packaged CLI entry points.
- Read [`AGENTS.md`](../AGENTS.md) and [`docs/agent-resume.md`](../docs/agent-resume.md) before security-sensitive DB work.
