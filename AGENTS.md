# AGENTS.md

## GitHub Identity

- This repo must use the GitHub account `aarshps` for GitHub operations. Do not use the global `aps_uhg` profile in this repo.
- Git commits in this repo should use `Aarsh <aarshps@users.noreply.github.com>` unless the user asks for a different author identity.
- This repo is part of the `/Users/aps/Source/aarshps` workspace and should use the shared GitHub CLI profile at `/Users/aps/Source/aarshps/.gh-aarshps`.
- For direct GitHub CLI commands, use `./scripts/gh-aarshps ...`. This wrapper points `gh` at the shared workspace profile.
- Do not run plain `gh ...` in this repo. On this machine, plain `gh` still resolves to the global `aps_uhg` profile.
- GitHub-authenticated `git` commands in this repo should rely on the repo-local `.git/config` credential settings, which point GitHub auth to the shared workspace profile. Do not change the global `gh auth` account just to work in this repo.
- If shared workspace auth stops resolving `aarshps`, verify with `GH_CONFIG_DIR=/Users/aps/Source/aarshps/.gh-aarshps gh api user --jq .login`.

## Isolation

- Do not make Git or GitHub auth changes globally for this repo. Avoid editing `~/.gitconfig`, `~/.config/gh`, global credential helpers, or any machine-wide auth state.
- Shared auth for repos under `/Users/aps/Source/aarshps` is allowed and expected. Do not extend these rules or credentials outside that workspace unless the user explicitly asks.
- Do not modify sibling repos or their agent instructions unless the user explicitly asks for that repo to be changed.
- Assume other agents may be active in other repos with different GitHub accounts. Keep all auth, config, and workflow changes scoped to this repo unless the user explicitly broadens scope.

## Skill Authoring

- Skills created for this repo must be granular and focused. Each skill should do one narrow job well.
- Keep each `SKILL.md` to 100 lines or fewer. If a skill starts to exceed that, split it into smaller skills or move detail into `references/` or `scripts/`.
- Do not bundle multiple workflows, domains, or variants into one broad skill unless they are inseparable in practice.
- Keep the main skill file procedural and minimal. Put reusable implementation in scripts and detailed context in references.
