# Copyright 2026 CodeRank
# Licensed under the Apache License, Version 2.0 (the "License").
# See the LICENSE file at the repository root.

"""Shape tests for the CodeRank Reviewer workflow.

These tests verify the structural contract of app.agent without running
Gemini. They exist to catch regressions when we add new agents or rewire
the orchestrator in later slices.
"""

from __future__ import annotations

from google.adk import Workflow
from google.adk.agents import Agent

from app.agent import (
    poster,
    reader,
    resolver,
    reviewer,
    root_agent,
    skeptic,
)

EXPECTED_AGENT_NAMES: tuple[str, ...] = (
    "reader",
    "resolver",
    "reviewer",
    "skeptic",
    "poster",
)


def test_all_five_agents_are_agent_instances() -> None:
    """Every exported agent is an ADK Agent instance."""
    for agent in (reader, resolver, reviewer, skeptic, poster):
        assert isinstance(agent, Agent), f"{agent} is not an Agent"


def test_agents_have_expected_names() -> None:
    """Agent names match the pipeline order: Reader, Resolver, Reviewer, Skeptic, Poster."""
    actual = (reader.name, resolver.name, reviewer.name, skeptic.name, poster.name)
    assert actual == EXPECTED_AGENT_NAMES, (
        f"Agent names drifted. Expected {EXPECTED_AGENT_NAMES}, got {actual}. "
        "If this is intentional (rename), update EXPECTED_AGENT_NAMES."
    )


def test_root_agent_is_workflow() -> None:
    """The root_agent export is a Workflow, not a plain Agent."""
    assert isinstance(root_agent, Workflow), (
        "root_agent must be a Workflow so ADK 2.0 Beta dynamic orchestration engages."
    )


def test_root_agent_has_expected_name() -> None:
    """The workflow is named 'coderank_reviewer' (snake_case, matches observability labels)."""
    assert root_agent.name == "coderank_reviewer"


def test_agents_use_pinned_model() -> None:
    """Every agent targets gemini-3.1-pro so thinking_level and observability stay consistent."""
    for agent in (reader, resolver, reviewer, skeptic, poster):
        # model can be a string or a Gemini() config; we accept both
        model_id = agent.model if isinstance(agent.model, str) else agent.model.model
        assert model_id == "gemini-3.1-pro", (
            f"{agent.name} uses {model_id}; expected gemini-3.1-pro"
        )
