from pathlib import Path
from tempfile import TemporaryDirectory

from agents.harness.document_context import (
    load_project_documents,
    render_document_context,
)


def test_missing_docs_is_valid_empty_context(tmp_path) -> None:
    assert load_project_documents(tmp_path) == []
    assert render_document_context([]) == "- No docs found"


def test_title_fallback_excerpt_limit_and_explicit_status(tmp_path) -> None:
    docs = tmp_path / "docs" / "adr"
    docs.mkdir(parents=True)
    (docs / "stack.md").write_text("- **Estado:** Propuesta\n\n" + "x" * 300, encoding="utf-8")
    reference = load_project_documents(tmp_path)[0]
    assert reference.title == "stack"
    assert reference.status == "Propuesta"
    assert len(reference.excerpt) <= 180


def test_load_project_documents_discovers_docs_and_adrs() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        docs = root / "docs"
        adr = docs / "adr"
        adr.mkdir(parents=True)
        (docs / "observability.md").write_text(
            "# Observability\n\nPlan de metricas y logs.",
            encoding="utf-8",
        )
        (adr / "ADR-0001-stack.md").write_text(
            "# ADR-0001 - Stack\n\n## Estado\n\nAceptada · 2026-08-31",
            encoding="utf-8",
        )

        documents = load_project_documents(root)

    assert [document.path for document in documents] == [
        "docs/adr/ADR-0001-stack.md",
        "docs/observability.md",
    ]
    assert documents[0].category == "adr"
    assert documents[0].status == "Aceptada · 2026-08-31"
    assert documents[1].category == "project-doc"


def test_render_document_context_outputs_compact_references() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        docs = root / "docs"
        docs.mkdir()
        (docs / "conventional-commits.md").write_text(
            "# Conventional Commits\n\nReglas de commits.",
            encoding="utf-8",
        )

        context = render_document_context(load_project_documents(root))

    assert "`docs/conventional-commits.md`" in context
    assert "[project-doc]" in context
    assert "Conventional Commits" in context
