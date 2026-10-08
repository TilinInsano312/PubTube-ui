"""Readiness diagnostics for the frontend agentic factory."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from agents.contracts import ContractError, load_contracts

MINIMUM_PYTHON = (3, 10)
REQUIRED_SCRIPTS = {"dev", "build", "preview", "lint", "format", "format:check", "test"}
REQUIRED_DOCS = (
    "README.md",
    "AGENTS.md",
    "docs/architecture.md",
    "docs/agentic-development.md",
    "docs/design-system.md",
)


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    passed: bool
    detail: str


Runner = Callable[..., subprocess.CompletedProcess[str]]


def structural_checks(root: Path) -> list[DoctorCheck]:
    """Inspect required files, scripts and contracts without running suites."""

    checks = [
        DoctorCheck(
            "python version",
            sys.version_info >= MINIMUM_PYTHON,
            f"requires >= {MINIMUM_PYTHON[0]}.{MINIMUM_PYTHON[1]}; found {sys.version_info.major}.{sys.version_info.minor}",
        ),
        DoctorCheck("agents import", True, "agents package imported"),
    ]
    package_path = root / "package.json"
    lock_path = root / "package-lock.json"
    if package_path.is_file():
        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
            scripts = package.get("scripts", {})
            missing_scripts = sorted(REQUIRED_SCRIPTS - scripts.keys()) if isinstance(scripts, dict) else sorted(REQUIRED_SCRIPTS)
            checks.append(
                DoctorCheck(
                    "npm scripts",
                    not missing_scripts,
                    "all required scripts present" if not missing_scripts else f"missing: {', '.join(missing_scripts)}",
                )
            )
        except (OSError, json.JSONDecodeError) as error:
            checks.append(DoctorCheck("npm scripts", False, f"cannot read package.json: {error}"))
    else:
        checks.append(DoctorCheck("npm scripts", False, "package.json is missing"))
    checks.extend(
        [
            DoctorCheck("npm lockfile", lock_path.is_file(), "package-lock.json present" if lock_path.is_file() else "package-lock.json is missing"),
            DoctorCheck("Vite config", (root / "vite.config.ts").is_file(), "vite.config.ts present" if (root / "vite.config.ts").is_file() else "vite.config.ts is missing"),
            DoctorCheck("frontend source", (root / "src").is_dir(), "src/ present" if (root / "src").is_dir() else "src/ is missing"),
        ]
    )
    missing_docs = [path for path in REQUIRED_DOCS if not (root / path).is_file()]
    checks.append(
        DoctorCheck(
            "required documentation",
            not missing_docs,
            "all required documents present" if not missing_docs else f"missing: {', '.join(missing_docs)}",
        )
    )
    try:
        count = len(load_contracts(root / "tasks"))
        checks.append(DoctorCheck("task contracts", True, f"{count} contract(s) valid"))
    except (ContractError, OSError) as error:
        checks.append(DoctorCheck("task contracts", False, str(error)))
    return checks


def command_checks(root: Path, runner: Runner = subprocess.run) -> list[DoctorCheck]:
    """Run only repository-owned checks; task contract commands are never used."""

    commands = (
        ("frontend lint", ["npm", "run", "lint"]),
        ("frontend format", ["npm", "run", "format:check"]),
        ("frontend tests", ["npm", "run", "test"]),
        ("frontend build", ["npm", "run", "build"]),
        ("factory compile", [sys.executable, "-m", "compileall", "-q", "agents"]),
        ("factory tests", [sys.executable, "-m", "pytest", "-q", "agents/tests"]),
        ("contract CLI", [sys.executable, "-m", "agents.contracts", "tasks/"]),
    )
    results: list[DoctorCheck] = []
    for name, command in commands:
        try:
            completed = runner(
                command,
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=180,
                shell=False,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            results.append(DoctorCheck(name, False, f"could not complete: {type(error).__name__}"))
            continue
        if completed.returncode == 0:
            results.append(DoctorCheck(name, True, "exit code 0"))
        else:
            results.append(
                DoctorCheck(
                    name,
                    False,
                    f"exit code {completed.returncode}; run {' '.join(command)} directly for details",
                )
            )
    return results


def run_doctor(root: Path, *, static: bool, runner: Runner = subprocess.run) -> list[DoctorCheck]:
    """Return every required readiness check for the selected mode."""

    checks = structural_checks(root)
    if not static and all(check.passed for check in checks):
        checks.extend(command_checks(root, runner))
    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check PubTube-ui factory readiness.")
    parser.add_argument("--static", action="store_true", help="Run structural checks only")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    checks = run_doctor(args.project_root.resolve(), static=args.static)
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}")
    ready = bool(checks) and all(check.passed for check in checks)
    print("FACTORY READY" if ready else "FACTORY NOT READY")
    return 0 if ready else 1
