# coderank-mcp-sidecar

A thin MCP bridge to the CodeRank public HTTPS API. Deployed to Cloud Run when the Agent Runtime image cannot embed the `coderank` CLI binary directly (fallback path).

The primary integration is the agent calling the `coderank` CLI directly over stdio MCP inside the Agent Runtime container. This sidecar exists only as a remote-MCP alternative.

## Status

Placeholder directory. Implementation lands in a follow-up commit. Python + FastAPI + the official `mcp` SDK.
