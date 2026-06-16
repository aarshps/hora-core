# hora-core

Shared, reusable building blocks for the **Hora** family of apps.

This repository is the single home for anything that should be common across more
than one Hora app — brand and design tokens, cross-app conventions, shared agent
skills, and reusable tooling. If a thing belongs to exactly one app, it stays in
that app's repo; if two or more apps need it, it belongs here.

## The Hora family

| App | What it is | Repo |
| --- | --- | --- |
| **Varisankya** | Subscription & recurring-payment tracker | `varisankya` (android · ios · web) |
| **Pathivu** | Habit tracker | `pathivu` (android · ios · web) |
| _future siblings_ | — | — |

Each app is its own cross-platform monorepo and keeps an internal `shared/` folder
for **its own** Android/iOS/web contracts (e.g. `firestore.rules`, a domain `SPEC.md`,
golden test vectors). `hora-core` sits one level above that: it holds what is shared
**between apps**, not within one.

## What belongs here

```
hora-core/
├── brand/                  Visual identity shared by the whole family
│                           (Material 3 Expressive tokens, Malayalam wordmark /
│                           launcher-icon conventions, color & type scales)
├── docs/
│   ├── conventions.md      The shared stack and conventions every Hora app follows
│   └── agent-resume.md     Durable repo state + handoff notes for AI agents
├── templates/              Copy-and-customize starting points (e.g. shared/firebase)
└── .github/skills/         Agent skills shared across the family
```

**Belongs here:** design tokens and brand assets used by 2+ apps; conventions that
every app is expected to follow; agent skills/tooling reused across apps; shared
domain vocabulary.

**Does _not_ belong here:** anything specific to a single app (keep it in that app's
repo), and **never** secrets, keys, service-account JSON, or `google-services.json`.

## How apps consume hora-core

Today the shared material is documentation and assets, consumed by reference. As
concrete code modules are extracted, the consumption mechanism (git submodule vs. a
published artifact) will be decided per module and recorded in `docs/conventions.md`.

## For AI agents

Start with [`AGENTS.md`](AGENTS.md), then read `docs/agent-resume.md`. Repo-local
skills live under `.github/skills/<name>/SKILL.md`.
