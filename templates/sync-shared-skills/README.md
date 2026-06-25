# Shared-skill sync (per-app)

How a Hora app consumes the shared skills that live in
[`hora-core/.github/skills/`](../../.github/skills/). This is the family's chosen
mechanism: each app keeps a small script that copies the skills it uses from a local
hora-core checkout into the app's own skill directory, so an agent working only inside
the app checkout still sees them (its native skill dir is where it looks).

## Why a sync script (not a submodule or hand-copy)

- Apps disagree on skill-dir location (Pathivu `android/.claude/skills/`, Varisankya
  `android/.agent/skills/`); a copy-in keeps each app's own convention.
- Synced skills are **generated** — there's one source of truth (hora-core) and no
  drift, because the copies are overwritten on each run rather than edited in place.
- No submodule plumbing, and it works the same on every dev machine.

## Use it

1. Copy `sync_shared_skills.sh` into the app (e.g. `android/tools/` or the repo root).
   Add a line to the app's `.gitattributes` so the script keeps LF endings on every
   checkout (without it, a fresh clone on Windows with `core.autocrlf=true` rewrites it
   to CRLF and `bash` chokes on the `\r`):

   ```
   *.sh text eol=lf
   ```

   Then `git add --renormalize` the script once after adding the rule.
2. Edit the three values at the top:
    - `HORA_CORE` — path to the local hora-core checkout (default assumes the standard
      `C:/Users/Aarsh/Source/hora-core/hora-core`; override with the `HORA_CORE` env var).
   - `DEST` — this app's skill dir (`android/.claude/skills` or `android/.agent/skills`).
   - `SKILLS` — the shared skills this app actually consumes.
3. Run it. It overwrites each listed skill under `DEST/` and writes a
   `.hora-core-synced` manifest (source path, timestamp, hora-core commit).
4. Delete any old hand-maintained duplicate of those skills, then verify the agent
   still resolves them. Commit the customised script + the synced copies.

## Rules

- **Never hand-edit a synced skill in the app.** Edit it in hora-core and re-run.
- Only sync skills that are genuinely shared (in hora-core because 2+ apps need them).
  App-specific skills stay in the app and are not touched by this script.
- This is a same-machine dev convenience: it reads a local hora-core checkout. Keep
  that checkout reasonably current (`git pull`) before syncing.
