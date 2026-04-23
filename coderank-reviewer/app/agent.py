# ruff: noqa
# Copyright 2026 CodeRank
# Licensed under the Apache License, Version 2.0 (the "License").
# See the LICENSE file at the repository root.

"""CodeRank Reviewer agent graph.

Five specialized agents collaborate on each pull request, orchestrated
as an ADK 2.0 Beta Workflow:

    Reader -> Resolver -> Reviewer -> Skeptic -> Poster

This file defines the graph skeleton. Each agent currently carries a
placeholder instruction so the shape is verifiable in `agents-cli
playground` and unit tests. Real instructions, MCP toolsets, and the
Skeptic's RequestInput gate land in subsequent slices.
"""

from __future__ import annotations

import os

import google.auth
from google.adk import Context, Workflow
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.workflow import START, node

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

_MODEL = "gemini-3.1-pro"


reader = Agent(
    name="reader",
    model=_MODEL,
    instruction=(
        "You are the Reader. In later slices you will use the GitHub MCP "
        "toolset to fetch a pull request's metadata, diff, and list of "
        "changed external symbols. For now, respond with a short "
        "acknowledgement of the input you received."
    ),
)

resolver = Agent(
    name="resolver",
    model=_MODEL,
    instruction=(
        "You are the Resolver. In later slices you will call the CodeRank "
        "MCP server's resolve_symbol tool for every external symbol the "
        "Reader extracted, tagging each as resolved or not_found. For now, "
        "pass the Reader's output through with a short acknowledgement."
    ),
)

reviewer = Agent(
    name="reviewer",
    model=_MODEL,
    instruction=(
        "You are the Reviewer. In later slices you will draft pull request "
        "comments grounded in the surfaces the Resolver returned. Every "
        "draft must include a citation URL. No citation, no comment. For "
        "now, pass the Resolver's output through with a short "
        "acknowledgement."
    ),
)

skeptic = Agent(
    name="skeptic",
    model=_MODEL,
    instruction=(
        "You are the Skeptic. In later slices you will re-fetch every "
        "citation the Reviewer produced and verify that the cited surface "
        "actually supports the claim, rejecting any draft that does not "
        "hold up. This is the hallucination firewall. For now, pass the "
        "Reviewer's output through with a short acknowledgement."
    ),
)

poster = Agent(
    name="poster",
    model=_MODEL,
    instruction=(
        "You are the Poster. In later slices you will use the GitHub MCP "
        "toolset to publish the Skeptic's approved comments back to the "
        "pull request with a 'Grounded in:' citation footer. For now, "
        "emit a short summary of the state you received."
    ),
)


_AGENT_SEQUENCE: tuple[Agent, ...] = (reader, resolver, reviewer, skeptic, poster)


@node(name="coderank_reviewer_pipeline", rerun_on_resume=True)
async def coderank_reviewer_pipeline(ctx: Context, node_input: str) -> str:
    """Drive the five agents in order, passing state between them.

    The `node_input` parameter name is required: ADK's function-node binder
    looks for that exact name to forward the user's inbound message. Later
    slices will promote this to a typed payload (PR URL, head SHA, install ID)
    via a Pydantic model once the webhook path is in place.
    """

    state: str = node_input
    for agent in _AGENT_SEQUENCE:
        state = await ctx.run_node(agent, state)
    return state


root_agent = Workflow(
    name="coderank_reviewer",
    edges=[(START, coderank_reviewer_pipeline)],
)

app = App(
    root_agent=root_agent,
    # Must match the agent module's directory name ("app/"). The ADK CLI
    # auto-discovers agents by scanning agents_dir and uses the subdirectory
    # name as the session service key; any other value breaks session lookup.
    # Workflow(name="coderank_reviewer") above is the product-facing name
    # that appears in Playground, traces, and observability.
    name="app",
)
