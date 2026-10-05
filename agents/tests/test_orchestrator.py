from agents import (AcceptanceCriterion, AgentOrchestrator, AgentRun, ChangeTrace,
                    Decision, Phase, ValidationCheck, ValidationStatus)


def test_orchestrator_builds_default_phase_plan() -> None:
    orchestrator = AgentOrchestrator()

    plan = orchestrator.build_plan()

    assert [step.phase for step in plan] == [
        Phase.ANALYZE,
        Phase.PLAN,
        Phase.IMPLEMENT,
        Phase.VERIFY,
        Phase.REVIEW,
        Phase.DECIDE,
    ]
    assert plan[0].agent.id == "software_engineer"
    assert plan[3].agent.id == "qa_validator"
    assert plan[4].agent.id == "reviewer"
    assert plan[5].skill.id == "reporting"


def test_orchestrator_returns_next_step_for_run_phase() -> None:
    run = AgentRun(task="Validar orquestador.", phase=Phase.VERIFY)
    orchestrator = AgentOrchestrator()

    step = orchestrator.next_step(run)

    assert step.phase == Phase.VERIFY
    assert step.agent.id == "qa_validator"
    assert step.skill.id == "validation"


def test_complete_cycle_assigns_supported_skills_and_finishes_done() -> None:
    run = AgentRun("Documentar UI", acceptance_criteria=[AcceptanceCriterion("AC1", "Guia disponible")])
    orchestrator = AgentOrchestrator()
    phases = []

    def capture():
        step = orchestrator.next_step(run)
        assert run.phase in step.skill.phases
        phases.append(step.phase)

    capture()
    run.set_plan(["Documentar", "Validar", "Revisar"])
    capture()
    run.record_change(ChangeTrace("CHG-001", "AC1", "docs/agentic-development.md",
                                  "Guia", "inspection", ValidationStatus.PASS))
    capture()
    run.record_validation(ValidationCheck("inspection", ValidationStatus.PASS, "Revisado"))
    capture()
    run.record_review()
    capture()
    assert run.decide() == Decision.DONE
    capture()
    assert phases == list(Phase)
    assert orchestrator.next_step(run).agent.id == "documentation_curator"
