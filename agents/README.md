# Fábrica agéntica PubTube-ui

Adaptación de la fábrica de PubTube-Mod4 para preparar tareas frontend y
observabilidad sin desplegar Grafana.

- [Arquitectura de la fábrica](architecture.md): responsabilidades y extensión.
- [Arquitectura frontend](../docs/architecture.md): límites y decisiones de la UI.
- [Ciclo operativo](software-engineering-loop.md): análisis hasta decisión.
- [Core](core/loop.py): AC, evidencia, cambios, tests y reportes.
- [Perfiles](profiles/): ingeniería, review, QA y documentación.
- [Skills](skills/): inspección, implementación, validación, diff y reporte.
- [Orquestador](orchestrator/): asignación determinista por fase.
- [Harness](harness/): creación de AgentRun y contexto de `docs/`.
- [Tarea](templates/task-template.md) y [reporte](templates/agent-report-template.md).
- [Tests](tests/): ejecutables sin red externa.

Desde la raíz, ejecutar `python -m agents.harness.run_agent_loop "Objetivo" --ac "Resultado" --scope "agents/"`.
El comando genera un brief; no implementa la tarea ni prueba un AC por sí mismo.
Leer [AGENTS.md](../AGENTS.md), [arquitectura frontend](../docs/architecture.md) y
[guía](../docs/agentic-development.md) antes de editar.
