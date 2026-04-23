# ruff: noqa
# Copyright 2026 CodeRank
# Licensed under the Apache License, Version 2.0 (the "License").
# See the LICENSE file at the repository root.

"""CodeRank Reviewer agent.

Scaffold. The production pipeline is a five-node ADK 2.0 Beta workflow
(Reader -> Resolver -> Reviewer -> Skeptic -> Poster) grounded in the
CodeRank MCP server and the official GitHub MCP server.

This file currently ships the minimal stub needed for `agents-cli playground`
and `agents-cli install` to succeed. The multi-agent graph lands in a
subsequent commit.
"""

import os

import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


root_agent = Agent(
    name="coderank_reviewer",
    model=Gemini(
        model="gemini-3.1-pro",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are the CodeRank Reviewer. You review GitHub pull requests and "
        "comment only when a claim can be grounded in a CodeRank API surface. "
        "No citation, no comment."
    ),
    tools=[],
)

app = App(
    root_agent=root_agent,
    name="coderank-reviewer",
)
