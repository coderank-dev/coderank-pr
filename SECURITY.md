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
- Dependabot security alerts are enabled. Configuration lives in `.github/dependabot.yml`.
- Pre-commit hooks run `gitleaks`, `detect-private-key`, and `detect-aws-credentials` on every commit.
- CI runs the same checks on every pull request.

### LiteLLM transitive dependency

LiteLLM is included as a transitive dependency through:

```
google-adk[eval]==2.0.0b1
  -> google-cloud-aiplatform[evaluation]>=1.148.0
    -> litellm>=1.75.5,<=1.82.6
```

The `<=1.82.6` upper bound is set by Google's `google-cloud-aiplatform` package and we cannot relax it from this repository. Patched LiteLLM releases (>=1.83.0) fall outside that range, so `uv lock` cannot resolve them while we depend on `google-adk==2.0.0b1`.

CodeRank Reviewer never imports or invokes LiteLLM. The agent talks to Gemini exclusively via Vertex AI from `coderank-reviewer/app/fast_api_app.py` and `coderank-reviewer/app/agent.py`. The vulnerable code paths in the published LiteLLM CVEs (LiteLLM proxy server, OIDC userinfo handling, password hashing) are never exercised by our deployed code or our development workflow.

Active LiteLLM advisories at the time of writing (2026-04-25):

- CVE-2026-35030 (critical): OIDC userinfo cache key collision authentication bypass
- CVE-2026-35029 (high): Privilege escalation via unrestricted proxy configuration endpoint
- GHSA-69x8-hrgq-fjj8 (high): Password hash exposure and pass-the-hash bypass

Each advisory is dismissed in the GitHub Security tab with reason "Vulnerable code is not actually used in this project" and a comment linking back to this section. Direct LiteLLM updates are also skipped in `.github/dependabot.yml` so weekly Dependabot runs do not fail on the unresolvable upgrade.

We will revisit when `google-cloud-aiplatform` releases a version with a wider LiteLLM range. To audit, run:

```bash
grep -r "litellm\|LiteLLM" coderank-reviewer/app/
```

The expected output is empty.

## Secret management

- No secrets are stored in this repository.
- Environment variables are configured through Google Secret Manager in production.
- `.env.example` documents the required variables without real values.
