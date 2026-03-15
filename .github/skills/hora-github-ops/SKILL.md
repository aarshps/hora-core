---
name: hora-github-ops
description: Use for GitHub CLI or API work in this repo, including PRs, issues, notifications, Dependabot, and pushes that must use the aarshps workspace profile safely.
---

# Hora GitHub Ops

Use this skill when the task touches GitHub from this repo.

## Required Commands

- Run `./scripts/gh-aarshps ...`. Do not run plain `gh ...` here.
- If GitHub state matters, verify login with `./scripts/gh-aarshps api user --jq .login`.
- Keep GitHub auth scoped to `/Users/aps/Source/aarshps`. Do not edit global GH or Git config.

## Workflow

1. Start with `git status --short` so you know whether the tree is already dirty.
2. Use repo-scoped GitHub commands such as `pr list`, `issue view`, or `api`.
3. If you push, push from the current repo only and only when the user asked for that workflow.
4. If you close, dismiss, or mark something read, leave or preserve a short rationale when the action affects shared history.

## Checks

- For notifications, inspect unread threads before marking anything as read.
- For PR cleanup, confirm the PR is still relevant before closing it.
- Read `docs/agent-resume.md` when the task depends on recent repo history.
