---
name: hora-agent-discussions
description: Guidelines for Hora family app agents to communicate, coordinate, and align on session statuses via GitHub Discussions.
---

# Hora Agent Discussions Coordination

Use this skill at the beginning and end of every agent session to synchronize context across family apps (Varisankya, Pathivu, etc.) via GitHub Discussions.

## Ground Rules

1. **Always Check at Startup:** At the beginning of a session, query the latest discussions to catch up on sibling app updates or shared component changes.
2. **Always Post on Closing:** Before finishing, write a concise summary of your session's work (successes, blocks, version bumps, or shared resource changes).
3. **Use for Inter-Agent Queries:** If you have questions about Varisankya or shared assets in hora-core, open a discussion thread in the Q&A or General categories.
4. **Identify Yourself:** Every post and comment must end with a standard signature indicating the agent's identity, unique conversation ID, and host work environment (e.g., 'Pathivu Agent (<unique-id>), working from Beeyeswon').


## Programmatic Operations (GitHub API)

To query and post without needing a browser, use the GitHub GraphQL API:

### 1. Fetching Recent Discussions
```bash
# Query recent discussions
gh api graphql -f query='
query {
  repository(owner: "aarshps", name: "hora-core") {
    discussions(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        title
        url
        body
      }
    }
  }
}
'
```

### 2. Posting an Update
```bash
# Mutation to create a discussion
# Repository ID: R_kgDODBp3zg
# General Category ID: DIC_kwDODBp3zs4C_3Wd
gh api graphql -f query='
mutation {
  createDiscussion(input: {
    repositoryId: "R_kgDODBp3zg"
    categoryId: "DIC_kwDODBp3zs4C_3Wd"
    title: "Pathivu/Varisankya: Session Update"
    body: "Summary details go here"
  }) {
    discussion {
      url
    }
  }
}
'
```