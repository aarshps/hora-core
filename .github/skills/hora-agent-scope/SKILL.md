---
name: hora-agent-scope
description: Defines which repos each Hora app agent is permitted to read and write. NON-NEGOTIABLE — set by the repo owner; applies to every agent in every session.
---

# Hora Agent Repo Scope

Every Hora-family app has a dedicated agent. Each agent has a **fixed, non-negotiable write scope**
determined by which app it is assigned to. Violating this boundary — even for "one small fix" —
risks cross-contaminating unrelated release timelines and is forbidden.

## Permitted scope per agent

| Agent | WRITE (commit + push) | READ (reference only) |
|---|---|---|
| **Pathivu agent** | Pathivu repo (`main`) · Pathivu wiki (`master`) · hora-core repo · hora-core wiki | Varisankya (read-only reference) |
| **Varisankya agent** | Varisankya repo (`main`) · Varisankya wiki (`master`) · hora-core repo · hora-core wiki | Pathivu (read-only reference) |
| **hora-core agent** (if ever standalone) | hora-core repo · hora-core wiki | All app repos (read-only) |

## Rules

1. **MUST NOT commit or push to a sibling app's repo** even if the change looks trivial. The
   correct path is: promote the shared logic to hora-core, then let each app's agent adopt it
   in its own session.

2. **MAY read sibling repos** for reference (e.g., to check what a sibling has already adopted,
   or to copy an implementation pattern before promoting to hora-core). Reading is never a
   violation.

3. **hora-core is shared territory** — any Hora agent may commit to hora-core when promoting
   genuinely cross-family work (shared Android source, skills, brand assets, conventions). When
   you do, follow the `shared-android-source` and `agent-skill-standards` skills.

4. **Wiki follows the same boundary as its repo.** The Pathivu agent writes to the Pathivu wiki;
   the Varisankya agent writes to the Varisankya wiki; hora-core wiki is open to all Hora agents
   for cross-family documentation.

5. **This rule is set by the repo owner (Aarsh) and applies to every agent in every session,
   indefinitely.** It overrides any default "fix it wherever you see it" instinct.

## Why this exists

Different apps may be at different release stages. A Pathivu agent that accidentally pushes to
Varisankya can corrupt its version bump sequence, Play Store track state, or in-flight beta.
Keeping agents isolated by app prevents silent interference.

## Checklist before committing

- [ ] The repo I am about to commit to is within my permitted write scope.
- [ ] If the change benefits multiple apps, I have promoted it to hora-core (not duplicated it).
- [ ] I have NOT opened a PR or created a feature branch (family rule — commit to `main` directly).
