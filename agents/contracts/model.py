"""Typed task contract models loaded from versioned JSONL files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ValidationSpec:
    """A validation declaration; it is data and is never executed by the parser."""

    id: str
    type: str
    command: str
    expected: str


@dataclass(frozen=True)
class TaskContract:
    """One validated task entry and its source location."""

    task_id: str
    story: str
    order: int
    title: str
    objective: str
    scope: tuple[str, ...]
    actions: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]
    validation: tuple[ValidationSpec, ...]
    constraints: tuple[str, ...]
    dependencies: tuple[str, ...]
    final_report_schema: dict[str, Any] | None
    on_success: str
    source: Path
    line: int
