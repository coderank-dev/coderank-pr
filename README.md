# CodeRank Reviewer

**An AI code review agent that cites its sources. Every comment grounded in real library documentation. No citation, no comment.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![CI](https://github.com/coderank-dev/coderank-pr/actions/workflows/ci.yml/badge.svg)](https://github.com/coderank-dev/coderank-pr/actions)
[![Secrets scan](https://github.com/coderank-dev/coderank-pr/actions/workflows/secrets-scan.yml/badge.svg)](https://github.com/coderank-dev/coderank-pr/actions)

---

## Why this exists

AI code review tools are here, they work, and they hallucinate. Published audits of the category leaders:

- **CodeRabbit:** 28% of review comments flagged as noise or incorrect assumptions (Lychee, 2025).
- **GitHub Copilot:** suggests non-existent npm packages ~15% of the time.
- **Stack Overflow 2025 developer survey:** AI trust dropped 11 points year over year to 29%, despite 84% usage.

Every tool in the top 10 grounds review comments in the codebase graph or in training data. None ground them in **external library documentation**. The result: confident suggestions to call methods that do not exist in the library version you actually use.

CodeRank Reviewer closes that gap. It reviews pull requests using a grounded multi-agent pipeline where every finding traces back to a real API surface entry, verified at comment time. If the agent cannot ground a claim, it does not post the comment.

The contract is simple:

> **If we post a comment about a library API, that API exists, at that version, with the semantics described.**

---

## How it works

CodeRank Reviewer is a multi-agent system built on Google's [Agent Development Kit (ADK)](https://adk.dev/) and deployed on [Agent Runtime](https://cloud.google.com/gemini-enterprise-agent-platform). Five specialized agents collaborate on each pull request:

```
  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐   ┌────────┐
  │  Reader │ → │ Resolver │ → │ Reviewer │ → │ Skeptic │ → │ Poster │
  └─────────┘   └──────────┘   └──────────┘   └─────────┘   └────────┘
       │             │              │              │             │
    GitHub        CodeRank       CodeRank       CodeRank      GitHub
     MCP           MCP           MCP            MCP           MCP
```

| Agent | Responsibility |
|-------|----------------|
| **Reader** | Fetches the PR diff via GitHub MCP. Extracts external imports and call sites. |
| **Resolver** | Resolves every symbol against the CodeRank API surface for the exact library version. Unresolvable symbols become high-confidence findings. |
| **Reviewer** | Produces draft comments. Each draft must include a citation URL pointing at the CodeRank surface line that supports the claim. |
| **Skeptic** | Re-fetches each cited surface line and verifies the claim is actually supported. Rejects any draft that fails. This is the hallucination firewall. |
| **Poster** | Posts approved comments via GitHub MCP with a "Grounded in: ..." citation footer. Adds a coverage summary listing reviewed vs skipped symbols. |

Every draft that reaches `Poster` has been grounded twice: once at generation, once at verification. That is the structural reason we cannot hallucinate.

---

## Powered by CodeRank

The grounding source is [CodeRank](https://coderank.ai), an AI-optimized library documentation system that serves token-efficient API surfaces for hundreds of libraries across versions.

CodeRank Reviewer uses CodeRank in two complementary ways:

1. **`coderank mcp-server`** runs inside the Agent Runtime container. Agents call it over stdio MCP to resolve symbols, fetch surfaces, and diff versions.
2. **`https://api.coderank.ai`** serves the authoritative data behind those calls.

You can try CodeRank yourself:

```bash
brew install --cask coderank-dev/tap/coderank
coderank query pydantic 2.9
```

The same binary the agent uses is one command away for any developer.

---

## Google Cloud stack

CodeRank Reviewer is built natively on Google's agent platform. The submission targets Track 1 of the Google for Startups AI Agents Challenge.

| Capability | Google product |
|------------|----------------|
| Agent framework | Agent Development Kit (ADK Python) |
| Scaffolding, eval, deploy | Agents CLI |
| Reasoning | Gemini 2.5 Pro via Vertex AI |
| Managed runtime | Agent Runtime on Gemini Enterprise Agent Platform |
| Webhook + MCP wrapper host | Cloud Run |
| CI/CD | Cloud Build, Developer Connect, GitHub Actions |
| Container images | Artifact Registry |
| Message queue | Pub/Sub |
| Secrets | Secret Manager |
| Observability | Cloud Trace, Cloud Logging |
| Evaluation | Agents CLI `eval run`, Agent Simulation |
| Agent-to-agent interop | A2A Protocol |
| Optional grounding fallback | Vertex AI Search |
| Distribution | Gemini Enterprise Marketplace |

---

## Quickstart

### Install the Agents CLI

```bash
uvx google-agents-cli setup
```

### Clone and configure

```bash
git clone https://github.com/coderank-dev/coderank-pr.git
cd coderank-pr
agents-cli install
cp .env.example .env
# fill in GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, GITHUB_TOKEN, CODERANK_API_KEY
```

### Run locally

```bash
# Start the CodeRank MCP sidecar
coderank mcp-server &

# Exercise the agent against a fixture PR
agents-cli run "Review PR https://github.com/coderank-dev/coderank-pr-demo/pull/1"
```

### Deploy to Google Cloud

```bash
agents-cli scaffold enhance --deployment-target agent_runtime
agents-cli infra single-project
agents-cli deploy
```

Full deploy guide in [docs/deploy.md](docs/deploy.md).

---

## Evaluation

The agent ships with an evalset covering:

- Pydantic v1 patterns in v2 projects (should flag with citation)
- Correct v2 usage (should not comment)
- Non-existent method calls (should flag as high-confidence bugs)
- Deprecated APIs (should flag with deprecation note from surface)
- Grounding-gap cases (should silently skip, not confabulate)

Run the evalset:

```bash
agents-cli eval run
```

Compare two runs after a prompt change:

```bash
agents-cli eval compare evals/run_v1.json evals/run_v2.json
```

---

## Architecture

Detailed architecture and deployment topology in [docs/architecture.md](docs/architecture.md).

Three deployed services:

1. **`coderank-reviewer`** - the 5-agent ADK workflow on Agent Runtime.
2. **`coderank-webhook`** - GitHub webhook receiver on Cloud Run; validates HMAC, publishes to Pub/Sub, invokes the agent.
3. **`coderank-mcp-sidecar`** - a thin MCP bridge to the CodeRank public API on Cloud Run, used when the Agent Runtime image cannot embed the CLI binary directly.

The Agent Runtime container bakes in the `coderank` CLI for direct stdio MCP use. The Cloud Run sidecar exists as a fallback path.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution contract. The short version: this repository consumes CodeRank only through its public CLI binary and its public HTTPS API. PRs that add direct imports of private CodeRank packages, or that leak internal URLs, IDs, prompts, or credentials, will be closed.

Security issues: see [SECURITY.md](SECURITY.md).

---

## License

Apache License 2.0. See [LICENSE](LICENSE).

---

## Acknowledgments

Built for the [Google for Startups AI Agents Challenge](https://devpost.team/google-cloud-for-startups/hackathons/3197), April to June 2026.
