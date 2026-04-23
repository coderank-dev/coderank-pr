# Security Policy

## Supported versions

CodeRank Reviewer is actively developed. The `main` branch receives security updates.

## Reporting a vulnerability

If you believe you have found a security vulnerability, please do not open a public issue.

Instead, email: `security@coderank.ai`

Include:

- A description of the vulnerability
- Steps to reproduce
- Affected commit SHA or release version
- Your assessment of the impact

We aim to respond within 48 hours and to have a mitigation in `main` within 7 days for high-severity issues.

## Scope

This repository consumes CodeRank only through its public CLI binary and its public HTTPS API at `https://api.coderank.ai`. It does not contain or import CodeRank's internal source, indexing pipeline, scoring logic, or infrastructure configuration.

Reports about the CodeRank platform itself (not this agent) should go to `security@coderank.ai` with a subject line mentioning the platform rather than the agent.

## Dependency hygiene

- Dependencies are pinned in `pyproject.toml` via `uv lock`.
- Dependabot security alerts are enabled.
- Pre-commit hooks run `gitleaks`, `detect-private-key`, and `detect-aws-credentials` on every commit.
- CI runs the same checks on every pull request.

## Secret management

- No secrets are stored in this repository.
- Environment variables are configured through Google Secret Manager in production.
- `.env.example` documents the required variables without real values.
