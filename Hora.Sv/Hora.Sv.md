# Hora.Sv

- Backend solution lives in `Hora.Sv/Hora`.
- `Hora.Web` is the ASP.NET Core web app; `Hora.Db.Ef` contains EF entities, context, and repositories.
- Main startup files are `Hora.Web/Program.cs` and `Hora.Web/Startup.cs`.
- Example API surface is in `Hora.Web/Controllers/TimeController.cs`.
- Keep runtime secrets out of `appsettings*.json`; use placeholders or local-only values.
- Read [`AGENTS.md`](../AGENTS.md) and [`docs/agent-resume.md`](../docs/agent-resume.md) before resuming repo work.
