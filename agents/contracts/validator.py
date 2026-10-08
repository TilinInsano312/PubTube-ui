"""Parse and validate task contracts without executing declared commands."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .model import TaskContract, ValidationSpec

REQUIRED_FIELDS = {
    "task_id",
    "story",
    "order",
    "title",
    "objective",
    "scope",
    "actions",
    "acceptance_criteria",
    "validation",
    "constraints",
    "dependencies",
    "on_success",
}
OPTIONAL_FIELDS = {"final_report_schema"}
VALIDATION_FIELDS = {"id", "type", "command", "expected"}
ALLOWED_ON_SUCCESS = {"CONTINUE", "DONE"}


class ContractError(ValueError):
    """Base class for actionable contract diagnostics."""


class ContractSyntaxError(ContractError):
    """Raised when a JSONL line is not valid JSON."""


class ContractSchemaError(ContractError):
    """Raised when a decoded entry does not match the contract schema."""


class ContractGraphError(ContractError):
    """Raised when IDs or dependencies do not form a valid graph."""


def _location(path: Path, line: int) -> str:
    return f"{path}:{line}"


def _non_empty_string(value: Any, field: str, path: Path, line: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractSchemaError(f"{_location(path, line)}: {field} must be a non-empty string")
    return value


def _string_list(
    value: Any,
    field: str,
    path: Path,
    line: int,
    *,
    non_empty: bool = False,
) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ContractSchemaError(f"{_location(path, line)}: {field} must be a list of strings")
    if non_empty and not value:
        raise ContractSchemaError(f"{_location(path, line)}: {field} must not be empty")
    result: list[str] = []
    for index, item in enumerate(value):
        result.append(_non_empty_string(item, f"{field}[{index}]", path, line))
    return tuple(result)


def _validation_specs(value: Any, path: Path, line: int) -> tuple[ValidationSpec, ...]:
    if not isinstance(value, list) or not value:
        raise ContractSchemaError(f"{_location(path, line)}: validation must be a non-empty list")
    specs: list[ValidationSpec] = []
    for index, item in enumerate(value):
        field = f"validation[{index}]"
        if not isinstance(item, dict):
            raise ContractSchemaError(f"{_location(path, line)}: {field} must be an object")
        missing = VALIDATION_FIELDS - item.keys()
        if missing:
            names = ", ".join(sorted(missing))
            raise ContractSchemaError(f"{_location(path, line)}: {field} missing fields: {names}")
        unknown = item.keys() - VALIDATION_FIELDS
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ContractSchemaError(f"{_location(path, line)}: {field} has unknown fields: {names}")
        specs.append(
            ValidationSpec(
                id=_non_empty_string(item["id"], f"{field}.id", path, line),
                type=_non_empty_string(item["type"], f"{field}.type", path, line),
                command=_non_empty_string(item["command"], f"{field}.command", path, line),
                expected=_non_empty_string(item["expected"], f"{field}.expected", path, line),
            )
        )
    return tuple(specs)


def _parse_entry(value: Any, path: Path, line: int) -> TaskContract:
    if not isinstance(value, dict):
        raise ContractSchemaError(f"{_location(path, line)}: contract entry must be a JSON object")
    missing = REQUIRED_FIELDS - value.keys()
    if missing:
        names = ", ".join(sorted(missing))
        raise ContractSchemaError(f"{_location(path, line)}: missing required fields: {names}")
    unknown = value.keys() - REQUIRED_FIELDS - OPTIONAL_FIELDS
    if unknown:
        names = ", ".join(sorted(unknown))
        raise ContractSchemaError(f"{_location(path, line)}: unknown fields: {names}")
    final_report_schema = None
    if "final_report_schema" in value:
        if not isinstance(value["final_report_schema"], dict):
            raise ContractSchemaError(
                f"{_location(path, line)}: final_report_schema must be a JSON object"
            )
        final_report_schema = value["final_report_schema"]
    order = value["order"]
    if isinstance(order, bool) or not isinstance(order, int) or order < 0:
        raise ContractSchemaError(f"{_location(path, line)}: order must be a non-negative integer")
    on_success = _non_empty_string(value["on_success"], "on_success", path, line)
    if on_success not in ALLOWED_ON_SUCCESS:
        allowed = ", ".join(sorted(ALLOWED_ON_SUCCESS))
        raise ContractSchemaError(
            f"{_location(path, line)}: on_success must be one of {allowed}; got {on_success!r}"
        )
    return TaskContract(
        task_id=_non_empty_string(value["task_id"], "task_id", path, line),
        story=_non_empty_string(value["story"], "story", path, line),
        order=order,
        title=_non_empty_string(value["title"], "title", path, line),
        objective=_non_empty_string(value["objective"], "objective", path, line),
        scope=_string_list(value["scope"], "scope", path, line, non_empty=True),
        actions=_string_list(value["actions"], "actions", path, line, non_empty=True),
        acceptance_criteria=_string_list(
            value["acceptance_criteria"], "acceptance_criteria", path, line, non_empty=True
        ),
        validation=_validation_specs(value["validation"], path, line),
        constraints=_string_list(value["constraints"], "constraints", path, line),
        dependencies=_string_list(value["dependencies"], "dependencies", path, line),
        final_report_schema=final_report_schema,
        on_success=on_success,
        source=path,
        line=line,
    )


def parse_contract_file(path: str | Path) -> list[TaskContract]:
    """Parse one JSONL file and validate each line structurally."""

    source = Path(path)
    contracts: list[TaskContract] = []
    with source.open(encoding="utf-8") as stream:
        for line_number, raw_line in enumerate(stream, start=1):
            if not raw_line.strip():
                continue
            try:
                decoded = json.loads(raw_line)
            except json.JSONDecodeError as error:
                raise ContractSyntaxError(
                    f"{_location(source, line_number)}: invalid JSON at column {error.colno}: {error.msg}"
                ) from error
            contracts.append(_parse_entry(decoded, source, line_number))
    return contracts


def validate_graph(contracts: Iterable[TaskContract]) -> list[TaskContract]:
    """Validate unique IDs, dependency existence and acyclicity."""

    entries = list(contracts)
    by_id: dict[str, TaskContract] = {}
    for contract in entries:
        previous = by_id.get(contract.task_id)
        if previous is not None:
            raise ContractGraphError(
                f"{_location(contract.source, contract.line)}: duplicate task_id {contract.task_id!r}; "
                f"first declared at {_location(previous.source, previous.line)}"
            )
        by_id[contract.task_id] = contract

    for contract in entries:
        for dependency in contract.dependencies:
            if dependency not in by_id:
                raise ContractGraphError(
                    f"{_location(contract.source, contract.line)}: task {contract.task_id!r} "
                    f"depends on unknown task_id {dependency!r}"
                )

    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(task_id: str) -> None:
        marker = state.get(task_id, 0)
        if marker == 2:
            return
        if marker == 1:
            cycle_start = stack.index(task_id)
            cycle = stack[cycle_start:] + [task_id]
            contract = by_id[task_id]
            raise ContractGraphError(
                f"{_location(contract.source, contract.line)}: dependency cycle detected: "
                + " -> ".join(cycle)
            )
        state[task_id] = 1
        stack.append(task_id)
        for dependency in by_id[task_id].dependencies:
            visit(dependency)
        stack.pop()
        state[task_id] = 2

    for task_id in by_id:
        visit(task_id)
    return entries


def load_contracts(path: str | Path) -> list[TaskContract]:
    """Load a JSONL file or every JSONL file in a directory as one collection."""

    target = Path(path)
    if target.is_dir():
        files = sorted(target.glob("*.jsonl"))
        if not files:
            raise ContractSchemaError(f"{target}: no .jsonl files found")
    elif target.is_file():
        files = [target]
    else:
        raise ContractSchemaError(f"{target}: path does not exist or is not a file/directory")
    contracts = [contract for file in files for contract in parse_contract_file(file)]
    return validate_graph(contracts)
