from agents import (
    AcceptanceCriterion,
    AgentRun,
    ChangeTrace,
    Decision,
    TestSummary as Summary,
    ValidationCheck,
    ValidationStatus,
)


def test_decide_done_when_all_acceptance_criteria_are_verified() -> None:
    run = AgentRun(
        task="Agregar documentacion agentica.",
        acceptance_criteria=[
            AcceptanceCriterion("AC1", "Existe una guia operativa."),
        ],
    )

    run.record_change(
        ChangeTrace(
            id="CHG-001",
            requirement="AC1",
            file="agents/software-engineering-loop.md",
            change="Documenta el ciclo agentico.",
            validation="revision de archivo",
            result=ValidationStatus.PASS,
        )
    )
    run.record_validation(
        ValidationCheck(
            name="revision de archivo",
            result=ValidationStatus.PASS,
            evidence="archivo presente",
        )
    )

    run.record_review()
    assert run.decide() == Decision.DONE


def test_decide_continue_when_acceptance_criterion_is_missing() -> None:
    run = AgentRun(
        task="Agregar pruebas del ciclo.",
        acceptance_criteria=[
            AcceptanceCriterion("AC1", "Existe implementacion."),
            AcceptanceCriterion("AC2", "Existe validacion."),
        ],
    )
    run.record_change(
        ChangeTrace(
            id="CHG-001",
            requirement="AC1",
            file="agents/agentic_loop.py",
            change="Agrega estructuras base.",
            validation="pytest agents/tests",
            result=ValidationStatus.PASS,
        )
    )

    run.record_validation(ValidationCheck("pytest agents/tests", ValidationStatus.PASS, "Tests ejecutados"))
    assert run.decide() == Decision.CONTINUE
    assert [criterion.id for criterion in run.missing_requirements()] == ["AC2"]


def test_render_final_report_includes_traceability_and_pending() -> None:
    run = AgentRun(task="Crear loop agentico ejecutable.")
    run.pending.append("Validacion manual pendiente.")
    run.set_test_summary(passed=3)

    report = run.render_final_report(Decision.CONTINUE)

    assert "## Status" in report
    assert "PARTIAL" in report
    assert "Crear loop agentico ejecutable." in report
    assert "Validacion manual pendiente." in report
    assert "Passed: 3" in report


def test_test_summary_defaults_to_zero() -> None:
    assert Summary() == Summary(passed=0, failed=0, skipped=0)


def completed_run() -> AgentRun:
    run = AgentRun("Documentar UI", acceptance_criteria=[AcceptanceCriterion("AC1", "Guia disponible")])
    run.record_change(ChangeTrace("CHG-001", "AC1", "docs/agentic-development.md",
                                  "Documentacion", "inspection", ValidationStatus.PASS))
    run.record_validation(ValidationCheck("inspection", ValidationStatus.PASS, "Guia revisada"))
    run.record_review()
    return run


def test_unverified_or_failed_check_prevents_done_and_can_be_retried() -> None:
    for result in (ValidationStatus.FAIL, ValidationStatus.NOT_VERIFIED):
        run = completed_run()
        run.record_validation(ValidationCheck("inspection", result, "Falta evidencia"))
        assert run.decide() == Decision.CONTINUE
        assert [ac.id for ac in run.missing_requirements()] == ["AC1"]
        run.record_validation(ValidationCheck("inspection", ValidationStatus.PASS, "Corregido y revisado"))
        assert run.decide() == Decision.DONE
        assert len(run.validations) == 3


def test_trace_without_passing_check_or_evidence_is_not_verified() -> None:
    run = completed_run()
    run.validations.clear()
    assert run.decide() == Decision.CONTINUE
    run.record_validation(ValidationCheck("inspection", ValidationStatus.PASS, " "))
    assert run.decide() == Decision.CONTINUE


def test_failed_tests_and_pending_prevent_done() -> None:
    run = completed_run()
    run.set_test_summary(passed=2, failed=1)
    assert run.decide() == Decision.CONTINUE
    run.set_test_summary(passed=3)
    run.pending.append("Resolver hallazgo")
    assert run.decide() == Decision.CONTINUE
    run.pending.clear()
    assert run.decide() == Decision.DONE


def test_review_required_and_new_change_invalidates_it() -> None:
    run = completed_run()
    run.reviewed = False
    assert run.decide() == Decision.CONTINUE
    run.record_review()
    run.record_change(ChangeTrace("CHG-002", "AC1", "docs/agentic-development.md",
                                  "Correccion", "inspection", ValidationStatus.PASS))
    assert run.decide() == Decision.CONTINUE
    run.record_review("Revisar enlaces")
    assert run.decide() == Decision.CONTINUE


def test_latest_trace_supersedes_old_passing_trace() -> None:
    run = completed_run()
    run.record_change(ChangeTrace("CHG-002", "AC1", "docs/agentic-development.md",
                                  "Revision pendiente", "inspection", ValidationStatus.NOT_VERIFIED))
    run.record_review()
    assert run.decide() == Decision.CONTINUE


def test_blocked_reason_is_reported_with_risks_decisions_and_limitations() -> None:
    run = completed_run()
    run.risks.append("Contrato pendiente")
    run.limitations.append("Sin servicio runtime")
    run.record_decision("Esperar contrato real")
    decision = run.decide(blocked_reason="Falta contrato aprobado")
    assert decision == Decision.BLOCKED
    report = run.render_final_report(decision)
    for value in ("BLOCKED", "Falta contrato aprobado", "Contrato pendiente",
                  "Sin servicio runtime", "Esperar contrato real", "AC1 -> PASS"):
        assert value in report


def test_empty_run_or_requested_done_without_evidence_stays_partial() -> None:
    run = AgentRun("Sin criterios")
    run.record_review()
    assert run.decide() == Decision.CONTINUE
    assert "PARTIAL" in run.render_final_report(Decision.DONE)


def test_report_distinguishes_failed_criterion_from_missing_evidence() -> None:
    run = completed_run()
    run.record_validation(ValidationCheck("inspection", ValidationStatus.FAIL, "Enlace roto"))
    assert "AC1 -> FAIL" in run.render_final_report(run.decide())
    run.record_validation(ValidationCheck("inspection", ValidationStatus.NOT_VERIFIED, "No disponible"))
    assert "AC1 -> NOT VERIFIED" in run.render_final_report(run.decide())
