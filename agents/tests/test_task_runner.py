from __future__ import annotations

import json
from pathlib import Path

from agents.harness.task_runner import render_task_brief, select_task


def test_task_runner_renders_all_operational_fields(tmp_path: Path) -> None:
    source = tmp_path / "task.jsonl"
    source.write_text(
        json.dumps(
            {
                "task_id": "TASK-1",
                "story": "TEST",
                "order": 0,
                "title": "Preparar brief",
                "objective": "Generar un brief completo",
                "scope": ["agents/"],
                "actions": ["Leer contrato"],
                "acceptance_criteria": ["Incluye todos los campos"],
                "validation": [
                    {"id": "V1", "type": "command", "command": "echo never", "expected": "No ejecutar"}
                ],
                "constraints": ["No ejecutar shell"],
                "dependencies": [],
                "on_success": "DONE",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    brief = render_task_brief(select_task(source, "TASK-1"))

    for expected in (
        "Objective: Generar un brief completo",
        "## Scope",
        "## Actions",
        "## Acceptance Criteria",
        "## Validation",
        "## Constraints",
        "## Dependencies",
        "## On Success",
        "Assigned agent:",
        "Skill:",
    ):
        assert expected in brief
    assert not (tmp_path / "never").exists()
