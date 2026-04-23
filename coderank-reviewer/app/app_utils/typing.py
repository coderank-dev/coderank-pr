# Copyright 2026 CodeRank
# Licensed under the Apache License, Version 2.0 (the "License").
# See the LICENSE file at the repository root.
import uuid
from typing import (
    Literal,
)

from pydantic import (
    BaseModel,
    Field,
)


class Feedback(BaseModel):
    """Represents feedback for a conversation."""

    score: int | float
    text: str | None = ""
    log_type: Literal["feedback"] = "feedback"
    service_name: Literal["coderank-reviewer"] = "coderank-reviewer"
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
