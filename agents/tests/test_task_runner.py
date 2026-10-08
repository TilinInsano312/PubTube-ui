from __future__ import annotations

import json
from pathlib import Path

from agents.harness import task_runner
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
                "final_report_schema": {
                    "status": "DONE | PARTIAL | BLOCKED",
                    "pending": ["pendiente o None"],
                },
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
        "## Final Report Schema",
        '"status": "DONE | PARTIAL | BLOCKED"',
        "Assigned agent:",
        "Skill:",
    ):
        assert expected in brief
    assert not (tmp_path / "never").exists()


def test_task_runner_has_no_implicit_scope_baseline(tmp_path: Path, monkeypatch) -> None:
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
                    {
                        "id": "V1",
                        "type": "inspection",
                        "command": "echo never",
                        "expected": "No ejecutar",
                    }
                ],
                "constraints": ["No ejecutar shell"],
                "dependencies": [],
                "on_success": "DONE",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    def unexpected_enforcement(*_args, **_kwargs):
        raise AssertionError("scope enforcement needs an explicit baseline")

    monkeypatch.setattr(task_runner, "enforce_scope", unexpected_enforcement)

    assert task_runner.main([str(source), "--task-id", "TASK-1"]) == 0
