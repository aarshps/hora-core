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
├── shared/                 Cross-app source modules consumed via per-app sync scripts
│   ├── android/            Kotlin utils + res design tokens (see shared/android/README.md)
│   ├── ios/                Swift services + views (see shared/ios/README.md)
│   └── web/                Next.js design system + components (see shared/web/README.md)
├── templates/              Copy-and-customize starting points (e.g. shared/firebase)
└── .github/skills/         Agent skills shared across the family
```

**Belongs here:** design tokens and brand assets used by 2+ apps; conventions that
every app is expected to follow; agent skills/tooling reused across apps; shared
domain vocabulary.

**Does _not_ belong here:** anything specific to a single app (keep it in that app's
repo), and **never** secrets, keys, service-account JSON, or `google-services.json`.

## How apps consume hora-core

Documentation, brand, and skills are consumed **by reference**. Concrete code modules
under `shared/{android,ios,web}/` are consumed as **generated copies**: each app runs a
small per-app sync script (`tools/sync_shared_android.sh`, `tools/sync_shared_ios.sh`,
`scripts/sync_shared_web.sh`) that copies the canonical files in, applies any token
substitution, and records provenance (source path, timestamp, hora-core commit) in a
`.hora-core-synced-*` manifest. Edit the canonical file here, then re-run the sync in each
app — never hand-edit the generated copy. See each `shared/<platform>/README.md`.

## For AI agents

Start with [`AGENTS.md`](AGENTS.md), then read `docs/agent-resume.md`. Repo-local
skills live under `.github/skills/<name>/SKILL.md`.
