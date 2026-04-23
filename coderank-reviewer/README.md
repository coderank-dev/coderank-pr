# coderank-reviewer

The multi-agent code review system. Scaffolded by `agents-cli` and deployed to Agent Runtime on Gemini Enterprise Agent Platform.

Five specialized agents collaborate on every pull request:

1. **Reader** reads the PR diff via GitHub MCP.
2. **Resolver** resolves every external symbol against CodeRank's API surface.
3. **Reviewer** drafts grounded review comments with citations.
4. **Skeptic** verifies each cited claim against the source surface, rejecting any draft that does not hold up.
5. **Poster** publishes approved comments with "Grounded in:" footers.

## Status

This directory is a placeholder. The ADK Python agent scaffold lands in a follow-up commit via `agents-cli create`. See the top-level [README](../README.md) for product context.
