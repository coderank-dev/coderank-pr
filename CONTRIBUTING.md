# Contributing to CodeRank Reviewer

Thanks for your interest. This repository is the public home of the CodeRank Reviewer agent, built for the Google for Startups AI Agents Challenge.

## Boundary

This repository consumes CodeRank only through two public surfaces:

1. The `coderank` CLI binary, distributed via Homebrew and GitHub Releases.
2. The public HTTPS API at `https://api.coderank.ai`.

It does not contain, import, or vendor:

- CodeRank's internal source (indexing pipeline, CLI source, API source, web app)
- Condensation prompts
- Health-scoring internals beyond what the public API surface exposes
- Any internal URLs, account IDs, or infrastructure identifiers
- Any credentials or secrets

Pull requests that add direct imports of private CodeRank packages, or that leak internal URLs, IDs, prompts, or credentials, will be closed without merging.

## Development setup

```bash
uvx google-agents-cli setup
git clone https://github.com/coderank-dev/coderank-pr.git
cd coderank-pr
agents-cli install
pre-commit install
cp .env.example .env
# fill in required values
```

## Running checks locally

```bash
pre-commit run --all-files
agents-cli lint
agents-cli eval run
```

## Pull request workflow

1. Fork or branch from `main`.
2. Make your changes with small, focused commits.
3. Ensure `pre-commit` hooks pass and all CI checks are green.
4. Open a PR with a clear description of the change and its motivation.
5. A maintainer will review.

## Commit style

Conventional commits:

```
feat: add skeptic hallucination filter
fix: handle missing surface for private symbols
docs: update README with Gemini Enterprise notes
refactor: extract citation builder into its own module
test: add evalset for pydantic v1 patterns
```

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0 (the same license as the project).

## Security

See [SECURITY.md](SECURITY.md) for how to report a security issue. Do not open public issues for suspected vulnerabilities.
