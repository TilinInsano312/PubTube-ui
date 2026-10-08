from __future__ import annotations

import json
from pathlib import Path

import pytest

from agents.contracts import (
    ContractGraphError,
    ContractSchemaError,
    ContractSyntaxError,
    load_contracts,
)


def contract(task_id: str = "TASK-1", **overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "task_id": task_id,
        "story": "TEST",
        "order": 0,
        "title": "Validar contrato",
        "objective": "Comprobar el parser",
        "scope": ["agents/"],
        "actions": ["Leer datos"],
        "acceptance_criteria": ["El contrato es válido"],
        "validation": [
            {"id": "V1", "type": "command", "command": "echo never", "expected": "No se ejecuta"}
        ],
        "constraints": ["No ejecutar comandos"],
        "dependencies": [],
        "on_success": "DONE",
    }
    value.update(overrides)
    return value


def write_jsonl(path: Path, *entries: dict[str, object]) -> Path:
    path.write_text("".join(json.dumps(entry) + "\n" for entry in entries), encoding="utf-8")
    return path


def test_valid_contract_is_loaded_without_executing_command(tmp_path: Path) -> None:
    marker = tmp_path / "must-not-exist"
    declared = f"touch {marker}"
    source = write_jsonl(
        tmp_path / "valid.jsonl",
        contract(validation=[{"id": "V1", "type": "command", "command": declared, "expected": "Nunca"}]),
    )

    loaded = load_contracts(source)

    assert loaded[0].validation[0].command == declared
    assert not marker.exists()


def test_invalid_json_reports_file_and_line(tmp_path: Path) -> None:
    source = tmp_path / "broken.jsonl"
    source.write_text('{"task_id":\n', encoding="utf-8")

    with pytest.raises(ContractSyntaxError, match=r"broken\.jsonl:1: invalid JSON"):
        load_contracts(source)


def test_duplicate_id_reports_both_locations(tmp_path: Path) -> None:
    source = write_jsonl(tmp_path / "duplicate.jsonl", contract(), contract())

    with pytest.raises(ContractGraphError, match="duplicate task_id"):
        load_contracts(source)


def test_missing_dependency_is_rejected(tmp_path: Path) -> None:
    source = write_jsonl(tmp_path / "missing.jsonl", contract(dependencies=["UNKNOWN"]))

    with pytest.raises(ContractGraphError, match="unknown task_id 'UNKNOWN'"):
        load_contracts(source)


def test_dependency_cycle_is_rejected(tmp_path: Path) -> None:
    source = write_jsonl(
        tmp_path / "cycle.jsonl",
        contract("A", dependencies=["B"]),
        contract("B", order=1, dependencies=["A"]),
    )

    with pytest.raises(ContractGraphError, match=r"dependency cycle detected: A -> B -> A"):
        load_contracts(source)


def test_invalid_on_success_is_a_schema_error(tmp_path: Path) -> None:
    source = write_jsonl(tmp_path / "status.jsonl", contract(on_success="MERGE"))

    with pytest.raises(ContractSchemaError, match="on_success must be one of"):
        load_contracts(source)


def test_unknown_contract_field_is_rejected(tmp_path: Path) -> None:
    source = write_jsonl(tmp_path / "unknown.jsonl", contract(surprise="ignored before"))

    with pytest.raises(ContractSchemaError, match="unknown fields: surprise"):
        load_contracts(source)


def test_unknown_validation_field_is_rejected(tmp_path: Path) -> None:
    source = write_jsonl(
        tmp_path / "unknown-validation.jsonl",
        contract(
            validation=[
                {
                    "id": "V1",
                    "type": "command",
                    "command": "echo never",
                    "expected": "No se ejecuta",
                    "surprise": True,
                }
            ]
        ),
    )

    with pytest.raises(ContractSchemaError, match="validation\\[0\\] has unknown fields: surprise"):
        load_contracts(source)


def test_final_report_schema_is_preserved(tmp_path: Path) -> None:
    schema = {"status": "DONE | PARTIAL | BLOCKED", "pending": ["item"]}
    source = write_jsonl(
        tmp_path / "report.jsonl",
        contract(final_report_schema=schema),
    )

    loaded = load_contracts(source)

    assert loaded[0].final_report_schema == schema
