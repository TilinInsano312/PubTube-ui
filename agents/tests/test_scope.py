from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from agents.scope import ScopeError, collect_changed_paths, is_path_authorized, unauthorized_paths


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, check=True, capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout.strip()


def test_exact_files_directories_and_outside_paths() -> None:
    scope = ["README.md", "agents/harness/"]

    assert is_path_authorized("README.md", scope)
    assert is_path_authorized("agents/harness/task_runner.py", scope)
    assert not is_path_authorized("agents/doctor.py", scope)
    assert unauthorized_paths(["README.md", "src/App.vue"], scope) == ["src/App.vue"]


def test_repository_scope_does_not_cover_high_impact_paths() -> None:
    assert is_path_authorized("src/App.vue", ["repository"])
    assert not is_path_authorized("package.json", ["repository"])
    assert not is_path_authorized(".github/workflows/ci.yml", ["repository"])
    assert not is_path_authorized("Dockerfile.dev", ["repository"])
    assert not is_path_authorized("docker-compose.yml", ["repository"])
    assert not is_path_authorized(".env.local", ["repository"])


def test_high_impact_paths_accept_explicit_scope() -> None:
    assert is_path_authorized("package.json", ["package.json"])
    assert is_path_authorized(".github/workflows/ci.yml", [".github/workflows/"])
    assert is_path_authorized("Dockerfile.dev", ["Dockerfile*"])
    assert is_path_authorized("docker-compose.test.yml", ["docker-compose*"])
    assert is_path_authorized(".env.example", [".env*"])


def test_collect_changed_paths_rejects_invalid_baseline(tmp_path: Path) -> None:
    git(tmp_path, "init")

    with pytest.raises(ScopeError, match="invalid Git baseline"):
        collect_changed_paths(tmp_path, "not-a-commit")


def test_collect_changed_paths_includes_all_git_states(tmp_path: Path) -> None:
    git(tmp_path, "init")
    git(tmp_path, "config", "user.email", "factory@example.invalid")
    git(tmp_path, "config", "user.name", "Factory Test")
    for name in ("committed.txt", "staged.txt", "unstaged.txt"):
        (tmp_path / name).write_text("base\n", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "initial")
    baseline = git(tmp_path, "rev-parse", "HEAD")

    (tmp_path / "committed.txt").write_text("committed\n", encoding="utf-8")
    git(tmp_path, "add", "committed.txt")
    git(tmp_path, "commit", "-m", "change committed file")
    (tmp_path / "staged.txt").write_text("staged\n", encoding="utf-8")
    git(tmp_path, "add", "staged.txt")
    (tmp_path / "unstaged.txt").write_text("unstaged\n", encoding="utf-8")
    (tmp_path / "untracked.txt").write_text("untracked\n", encoding="utf-8")

    assert collect_changed_paths(tmp_path, baseline) == {
        "committed.txt",
        "staged.txt",
        "unstaged.txt",
        "untracked.txt",
    }
