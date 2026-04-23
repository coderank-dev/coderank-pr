# Architecture

This document is a placeholder. Full architecture diagram and request-flow walkthrough land alongside the first working deployment.

## High-level

Three services deployed on Google Cloud:

| Service | Runtime | Purpose |
|---------|---------|---------|
| `coderank-reviewer` | Agent Runtime | 5-agent ADK workflow, invoked per PR |
| `coderank-webhook`  | Cloud Run     | GitHub webhook receiver (HMAC + Pub/Sub dispatch) |
| `coderank-mcp-sidecar` | Cloud Run  | Fallback MCP bridge to the CodeRank public API |

## Request flow

1. GitHub emits a `pull_request` webhook.
2. `coderank-webhook` validates the signature and publishes to Pub/Sub.
3. Agent Runtime triggers `coderank-reviewer`.
4. Agents call out via MCP to GitHub and to `coderank mcp-server` (running inside the same container).
5. Reviewer drafts comments grounded in CodeRank surfaces.
6. Skeptic re-verifies every citation.
7. Poster publishes approved comments back to the PR via GitHub MCP.

## Grounding contract

Every review comment includes a citation URL resolving to a CodeRank API surface entry. The Skeptic agent re-fetches each citation and verifies that the source actually supports the claim before the comment is posted. No citation, no comment.
