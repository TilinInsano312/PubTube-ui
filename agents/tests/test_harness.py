from agents.core import Phase
from pathlib import Path
import subprocess
import sys
from agents.harness.run_agent_loop import build_agent_run, render_run_brief


def test_build_agent_run_numbers_acceptance_criteria() -> None:
    run = build_agent_run(
        task="Ordenar agentes.",
        acceptance_criteria=["Existe catalogo.", "Existe orquestador."],
        scope=["agents/"],
    )

    assert run.phase == Phase.ANALYZE
    assert [criterion.id for criterion in run.acceptance_criteria] == ["AC1", "AC2"]
    assert run.scope == ["agents/"]


def test_render_run_brief_includes_next_agent_and_skill() -> None:
    run = build_agent_run(task="Preparar brief.", scope=["agents/"])

    brief = render_run_brief(run, include_docs=False)

    assert "Agent Run Brief" in brief
    assert "Software Engineering Agent" in brief
    assert "Repository Inspection" in brief
    assert "`agents/`" in brief


def test_render_run_brief_includes_project_docs_by_default() -> None:
    run = build_agent_run(task="Leer documentacion.")

    brief = render_run_brief(run)

    assert "## Project Documentation Context" in brief
    assert "`docs/agentic-development.md`" in brief


def test_cli_brief_and_partial_report_from_repository_root(tmp_path) -> None:
    root = Path(__file__).resolve().parents[2]
    command = [sys.executable, "-m", "agents.harness.run_agent_loop",
               "Validar fabrica agentica UI", "--ac", "Genera brief",
               "--scope", "agents/", "--project-root", str(tmp_path)]
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8", timeout=10)
    assert result.returncode == 0, result.stderr
    assert "AC1: Genera brief" in result.stdout
    assert "No docs found" in result.stdout
    result = subprocess.run(command + ["--final-report"], cwd=root,
                            capture_output=True, text=True, encoding="utf-8", timeout=10)
    assert result.returncode == 0, result.stderr
    assert "PARTIAL" in result.stdout
    assert "AC1 -> NOT VERIFIED" in result.stdout
