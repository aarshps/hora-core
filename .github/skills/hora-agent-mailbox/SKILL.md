---
name: hora-agent-mailbox
description: Local, same-machine mailbox for coordinating between concurrent AI agent sessions across Hora-family repos (hora-core, Pathivu, Varisankya, etc.). Use when picking up work that may overlap another session, or when landing something other repos' agents should know about.
---

# Hora agent mailbox

A gitignored drop-folder at `.agent-mailbox/` in this repo's root, used by AI agent
sessions on **this machine** to leave each other short, durable-ish notes. It exists
because there is no live inter-session messaging tool — this is the closest substitute.

## Scope and caveats — read first

- **Same-machine only.** Nothing under `.agent-mailbox/` is committed (`.gitignore`
  excludes it). A fresh clone, a CI runner, or a different machine will never see it.
  Don't rely on it for anything that must survive a clone.
- **Not a substitute for the durable record.** Once an action actually lands, the
  permanent account belongs in `docs/agent-resume.md` (hora-core) or the equivalent in
  another repo. Mailbox messages are ephemeral pings that something happened or is
  about to happen — write the real record separately, then optionally point to it here.
- **Not a substitute for asking the user.** Use this for agent-to-agent FYI/handoff
  traffic, never to make a decision on the user's behalf that needs their judgment.
- **No secrets.** Even though gitignored, treat every message as something a human
  could stumble into. No vault item names, project IDs, keys, or tokens.

## Layout

```
.agent-mailbox/
├── hora-core/        messages addressed to (or originating from) the hora-core agent
├── pathivu/          messages addressed to (or originating from) a Pathivu-repo agent
├── varisankya/        messages addressed to (or originating from) a Varisankya-repo agent
└── <other-repo-slug>/   one folder per repo, created on first use
```

Use the repo's actual folder name (lowercase) as the slug. Create a repo's folder the
first time you write to it — don't pre-create empty folders for repos you're not
messaging.

## Message format

One file per message, **write-once** — never edit or delete another session's message.
If a message needs a reply or an update, write a new file that supersedes it.

Filename: `<UTC-ISO-timestamp-with-hyphens>-<short-slug>.md`, e.g.
`2026-06-16T14-32-05Z-extraction-landed.md`. Colons are replaced with hyphens for
Windows filename safety; the timestamp also keeps concurrent writers collision-free and
gives a natural read order.

```markdown
---
from: hora-core
to: pathivu
status: open
---

One paragraph: what happened or what's needed, and where to look for the durable
record (a commit, a file path, a doc section) if there is one.
```

- `status: open` — needs action or acknowledgment from the recipient.
- `status: resolved` — informational, or a prior `open` message has been handled.
  Write a *new* file with `status: resolved` referencing the original by filename;
  don't mutate the original.
- `to: all` is fine for broadcast notes relevant to every family repo.

## Workflow

1. **On session start**, check your own repo's folder (and `to: all` messages in
   others, if you can see them) for anything `status: open`.
2. **When you land something other repos' agents should know about** — a shared
   asset extracted, a convention changed, a breaking rename — write a message to the
   relevant repo's folder (or `all`).
3. **When you act on an `open` message**, write a `resolved` follow-up rather than
   editing the original, so the history of who-said-what stays intact.
4. Mailbox messages are a *pointer*, not the source of truth — always also update the
   real docs (`docs/agent-resume.md` here, or the equivalent committed doc elsewhere)
   for anything that should outlive this machine.
