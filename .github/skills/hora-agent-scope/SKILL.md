---
name: hora-agent-scope
description: Defines exactly which repositories each Hora-family app agent is permitted to read and modify. Read this at session start to know your boundaries — touching a sibling app's repo is always out of scope.
---

# Hora Agent Scope

Each Hora-family app has its own dedicated agent. Every agent has a fixed scope —
it may only write to the repos listed under its own entry below.

## Permitted scope per agent

| Agent | May write to |
|-------|-------------|
| **Varisankya agent** | `varisankya` repo + wiki · `hora-core` repo + wiki |
| **Pathivu agent** | `pathivu-android` repo + wiki · `hora-core` repo + wiki |
| *(future app agents)* | `<app>` repo + wiki · `hora-core` repo + wiki |

**Every agent may write to hora-core.** It is the shared foundation — updating shared
components, skills, conventions, and the wiki is part of an agent's normal job.

**No agent writes to a sibling app's repo.** If you are the Varisankya agent, do not
open, stage, commit, or push anything in `pathivu-android/` (or any other sibling). The
same rule applies in reverse. This is unconditional — even if a change would "obviously
help" the sibling, leave it for that app's own agent.

## What counts as a sibling repo

Any directory under `C:\Users\Aarsh\Source\` that is not your own app repo or
`hora-core`. Examples: `pathivu-android/`, `pathivu-ios/`, `pathivu-web/`,
`aasthi/`, `vellam/`, `beeyeswon/`, etc.

## Crossing the boundary (when it looks tempting)

- **Promotion to hora-core** — if you improved a component that both apps share, promote
  the canonical version to `hora-core/shared/android/` (or the relevant shared path),
  commit it there, then let the sibling agent sync it on their next pass. Do **not** sync
  it into the sibling yourself.
- **Skill updates** — if you write or update a hora-core skill, it will be inherited by
  the sibling on their next `bash tools/sync_shared_skills.sh` run. You do not need to
  run that script in the sibling repo yourself.
- **Wiki cross-links** — you may edit the **hora-core wiki** to reference all apps, but
  you must not edit a sibling app's own wiki.

## Confirming your scope at session start

Before touching any file, verify you are working in the correct repo:

```
git remote -v        # confirms which repo you are in
```

If the output shows a sibling repo URL, stop and navigate to the correct directory.
