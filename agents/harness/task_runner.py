"""Prepare complete task briefs and optionally enforce their declared scope."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agents.contracts import ContractError, TaskContract, load_contracts
from agents.harness.run_agent_loop import build_agent_run, render_run_brief
from agents.scope import ScopeError, enforce_scope


def select_task(path: str | Path, task_id: str) -> TaskContract:
    """Load contracts and return the requested task."""

    matches = [contract for contract in load_contracts(path) if contract.task_id == task_id]
    if not matches:
        raise ContractError(f"task_id {task_id!r} was not found in {path}")
    return matches[0]


def _list(title: str, values: tuple[str, ...]) -> str:
    content = "\n".join(f"- {value}" for value in values) or "- None"
    return f"## {title}\n\n{content}"


def render_task_brief(contract: TaskContract) -> str:
    """Render every operational field plus the existing phase assignment."""

    run = build_agent_run(
        task=contract.objective,
        acceptance_criteria=list(contract.acceptance_criteria),
        scope=list(contract.scope),
    )
    validation = tuple(
        f"{item.id} [{item.type}]: `{item.command}` — expected: {item.expected}"
        for item in contract.validation
    )
    header = [
        f"Task ID: {contract.task_id}",
        f"Story: {contract.story}",
        f"Order: {contract.order}",
        f"Title: {contract.title}",
        f"Objective: {contract.objective}",
    ]
    sections = [
        render_run_brief(run, include_docs=False),
        "\n".join(header),
        _list("Actions", contract.actions),
        _list("Validation", validation),
        _list("Constraints", contract.constraints),
        _list("Dependencies", contract.dependencies),
        f"## On Success\n\n{contract.on_success}",
    ]
    return "\n\n".join(sections)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare a complete brief from a task JSONL contract.")
    parser.add_argument("path", help="Task JSONL file or directory")
    parser.add_argument("--task-id", required=True, help="Exact task_id to prepare")
    parser.add_argument("--baseline", help="Explicit Git baseline used to enforce changed-file scope")
    parser.add_argument("--repository", default=".", help="Repository root for scope enforcement")
    args = parser.parse_args(argv)
    try:
        contract = select_task(args.path, args.task_id)
        print(render_task_brief(contract))
        if args.baseline:
            changed = enforce_scope(args.repository, args.baseline, contract.scope)
            print(f"\n## Scope Check\n\nPASS: {len(changed)} changed path(s) authorized.")
    except (ContractError, ScopeError, OSError) as error:
        print(f"TASK RUNNER ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
