from __future__ import annotations

import json
import subprocess
from pathlib import Path

from agents.doctor import command_checks, run_doctor, structural_checks


def make_ready_root(root: Path) -> Path:
    scripts = {name: "unused" for name in ("dev", "build", "preview", "lint", "format", "format:check", "test")}
    (root / "package.json").write_text(json.dumps({"scripts": scripts}), encoding="utf-8")
    (root / "package-lock.json").write_text("{}", encoding="utf-8")
    (root / "vite.config.ts").write_text("export default {}\n", encoding="utf-8")
    (root / "src").mkdir()
    for relative in (
        "README.md",
        "AGENTS.md",
        "docs/architecture.md",
        "docs/agentic-development.md",
        "docs/design-system.md",
    ):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("required\n", encoding="utf-8")
    (root / "tasks").mkdir()
    contract = {
        "task_id": "TASK-1",
        "story": "TEST",
        "order": 0,
        "title": "Test",
        "objective": "Test doctor",
        "scope": ["agents/"],
        "actions": ["Inspect"],
        "acceptance_criteria": ["Ready"],
        "validation": [{"id": "V1", "type": "inspection", "command": "Never run", "expected": "Ready"}],
        "constraints": [],
        "dependencies": [],
        "on_success": "DONE",
    }
    (root / "tasks" / "test.jsonl").write_text(json.dumps(contract) + "\n", encoding="utf-8")
    return root


def test_static_doctor_is_ready_without_subprocess(tmp_path: Path) -> None:
    root = make_ready_root(tmp_path)

    def forbidden_runner(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("static doctor must not invoke subprocess")

    checks = run_doctor(root, static=True, runner=forbidden_runner)

    assert checks
    assert all(check.passed for check in checks)


def test_structural_failure_is_actionable(tmp_path: Path) -> None:
    root = make_ready_root(tmp_path)
    package = json.loads((root / "package.json").read_text(encoding="utf-8"))
    del package["scripts"]["lint"]
    (root / "package.json").write_text(json.dumps(package), encoding="utf-8")

    failed = [check for check in structural_checks(root) if not check.passed]

    assert failed[0].name == "npm scripts"
    assert failed[0].detail == "missing: lint"


def test_command_checks_use_safe_subprocess_arguments(tmp_path: Path) -> None:
    calls: list[tuple[list[str], dict[str, object]]] = []

    def fake_runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, stdout="SENSITIVE=fixture-only", stderr="")

    checks = command_checks(tmp_path, runner=fake_runner)

    assert all(check.passed for check in checks)
    assert calls
    assert all(kwargs["shell"] is False for _, kwargs in calls)
    assert all(kwargs["capture_output"] is True for _, kwargs in calls)
    assert all(kwargs["timeout"] == 180 for _, kwargs in calls)
    assert all("fixture-only" not in check.detail for check in checks)


def test_failed_command_does_not_echo_captured_secrets(tmp_path: Path) -> None:
    def failing_runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 1, stdout="SENSITIVE=fixture-only", stderr="private fixture")

    checks = command_checks(tmp_path, runner=failing_runner)

    assert all(not check.passed for check in checks)
    assert all("private" not in check.detail for check in checks)
