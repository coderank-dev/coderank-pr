# coderank-webhook

GitHub webhook receiver. Deployed to Cloud Run.

Validates the HMAC signature on incoming `pull_request` events, publishes a minimal event to Pub/Sub, and returns 202. The heavy lifting happens in `coderank-reviewer` on Agent Runtime.

## Status

Placeholder directory. Implementation lands in a follow-up commit. Python + FastAPI.
