"""Git-aware scope authorization for agentic task execution."""

from __future__ import annotations

import fnmatch
import subprocess
from collections.abc import Iterable
from pathlib import Path, PurePosixPath


class ScopeError(ValueError):
    """Raised when scope or baseline validation cannot proceed."""


def normalize_path(path: str) -> str:
    """Return a repository-relative POSIX path without unsafe parent traversal."""

    normalized = PurePosixPath(path.replace("\\", "/"))
    if normalized.is_absolute() or ".." in normalized.parts:
        raise ScopeError(f"path must be repository-relative: {path!r}")
    return normalized.as_posix().removeprefix("./")


def is_high_impact_path(path: str) -> bool:
    """Return whether a path needs explicit contract authorization."""

    normalized = normalize_path(path)
    name = PurePosixPath(normalized).name
    return (
        normalized in {"package.json", "package-lock.json"}
        or normalized.startswith(".github/workflows/")
        or name.startswith("Dockerfile")
        or name.startswith("docker-compose")
        or name == ".env"
        or name.startswith(".env.")
    )


def _entry_matches(path: str, entry: str) -> bool:
    normalized_path = normalize_path(path)
    normalized_entry = entry.replace("\\", "/").removeprefix("./")
    if normalized_entry.endswith("/"):
        return normalized_path.startswith(normalized_entry)
    if any(character in normalized_entry for character in "*?["):
        return fnmatch.fnmatchcase(normalized_path, normalized_entry)
    return normalized_path == normalize_path(normalized_entry)


def is_path_authorized(path: str, scope: Iterable[str]) -> bool:
    """Check exact files, declared directories and explicit glob patterns."""

    entries = tuple(scope)
    explicit_match = any(entry != "repository" and _entry_matches(path, entry) for entry in entries)
    if is_high_impact_path(path):
        return explicit_match
    return explicit_match or "repository" in entries


def unauthorized_paths(paths: Iterable[str], scope: Iterable[str]) -> list[str]:
    """Return sorted changed paths not authorized by scope."""

    entries = tuple(scope)
    return sorted({normalize_path(path) for path in paths if not is_path_authorized(path, entries)})


def _run_git(root: Path, arguments: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=20,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise ScopeError(f"git {' '.join(arguments)} failed: {detail}")
    return [line for line in result.stdout.splitlines() if line]


def collect_changed_paths(root: str | Path, baseline: str) -> set[str]:
    """Collect committed, staged, unstaged and untracked paths from a baseline."""

    repository = Path(root)
    try:
        _run_git(repository, ["rev-parse", "--verify", f"{baseline}^{{commit}}"])
    except ScopeError as error:
        raise ScopeError(f"invalid Git baseline {baseline!r}: {error}") from error
    groups = (
        _run_git(repository, ["diff", "--name-only", baseline, "HEAD"]),
        _run_git(repository, ["diff", "--cached", "--name-only"]),
        _run_git(repository, ["diff", "--name-only"]),
        _run_git(repository, ["ls-files", "--others", "--exclude-standard"]),
    )
    return {normalize_path(path) for group in groups for path in group}


def enforce_scope(root: str | Path, baseline: str, scope: Iterable[str]) -> set[str]:
    """Raise with remediation when any Git change falls outside task scope."""

    changed = collect_changed_paths(root, baseline)
    rejected = unauthorized_paths(changed, scope)
    if rejected:
        listed = ", ".join(rejected)
        raise ScopeError(
            f"files outside authorized scope: {listed}. Expand the task contract scope or revert those changes."
        )
    return changed
