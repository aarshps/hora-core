---
name: hora-github-ops
description: Use for GitHub CLI or API work in hora-core — PRs, issues, releases, archive/unarchive, and pushes that must run as the aarshps account.
---

# Hora GitHub Ops

Use this skill when the task touches GitHub from this repo.

## Identity

- This repo operates as the GitHub account **`aarshps`**.
- On this Windows machine, plain `gh` is already authenticated as `aarshps` (keyring).
  Use `gh ...` directly — there is no wrapper script here.
- Verify when identity matters: `gh api user --jq .login` (expect `aarshps`).
- Do not change global `gh`/git auth state.

## Common operations

- State of the repo: `gh repo view aarshps/hora-core --json isArchived,visibility,defaultBranchRef`.
- Unarchive (archived repos are read-only): `gh api -X PATCH repos/aarshps/hora-core -f archived=false`.
- PRs / issues: `gh pr list`, `gh issue view`, `gh api ...` as needed.

## Workflow

1. Start with `git status --short` so you know whether the tree is already dirty.
2. Make the change, then push to the branch the user named (often `main` here).
3. The wiki is a separate git repo (`hora-core.wiki.git`, default branch `master`).
4. When you close, dismiss, or mark something read, leave a short rationale if it
   affects shared history.

## Checks

- Confirm the repo is not archived before attempting a push.
- For notifications, inspect unread threads before marking anything read.
- Read `docs/agent-resume.md` when the task depends on recent repo history.
