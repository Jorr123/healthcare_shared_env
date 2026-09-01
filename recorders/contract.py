"""Recorder-neutral step data emitted by the shared Phase-3 runner."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RecorderStep:
    """One simulator step plus its shared FSM identity."""

    env: Any
    observation: Any
    action: Any
    stage_name: str
    stage_suffix: str
    step_id: int
    skill: str
