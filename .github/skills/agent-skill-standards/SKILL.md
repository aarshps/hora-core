---
name: agent-skill-standards
description: Guidelines for creating and maintaining granular, high-quality agent skills, shared across the Hora family.
---

# Agent Skill Standards

To maintain a high-quality codebase and a consistent AI pair-programming experience, skills must follow these standards. Applies to skills in any Hora app repo as well as here in `hora-core`.

## Granularity & Focus

1. **One topic per skill:** Avoid "General UI" or "Common Utils". Use specific titles like `Hero Section Stability` or `Currency Display Standards`.
2. **Minimal duplication:** If a rule applies to multiple components (e.g., currency formatting in charts and lists), create a single central skill and reference it.
3. **Actionable rules:** Skills must provide concrete "MUST" and "MUST NOT" rules, not just general descriptions.

## Structure

Every `SKILL.md` MUST follow this structure:
- **YAML frontmatter:** `name` and `description`.
- **Primary header:** title of the skill.
- **Rules/principles:** the core technical or design requirements.
- **Implementation examples:** snippets demonstrating the "correct" way.
- **Checklist:** a short list of verification items to ensure compliance.

## Evolution

1. **Context sync:** after completing a major feature or resolving a subtle bug, immediately extract that knowledge into a skill or update an existing one.
2. **Reversion documentation:** if a pattern is tried and reverted, update the relevant skill to document WHY the prior pattern was restored — don't just silently revert.

## Metadata guidelines

- Use clear, lowercase-hyphenated directory names matching `name:` in the frontmatter.
- Keep descriptions concise for quick indexing by the AI agent.

## Hora-family scope note

A skill belongs in an app's own repo if it documents that app's specific implementation (class names, package paths, one-off bugs). It only belongs in `hora-core` once it's been generalized to a convention 2+ apps actually share — see `docs/conventions.md` and the `hora-repo-map` skill for that boundary.
