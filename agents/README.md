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
- [Contratos](contracts/): parser y validador JSONL sin ejecución de comandos.
- [Scope](scope/): autorización de rutas y comprobación de cambios Git.
- [Tarea](templates/task-template.md) y [reporte](templates/agent-report-template.md).
- [Plantilla humana breve](templates/simple-task-template.md): entrada cotidiana
  sin necesidad de escribir JSONL.
- [Tests](tests/): ejecutables sin red externa.

Desde la raíz, ejecutar `python -m agents.harness.run_agent_loop "Objetivo" --ac "Resultado" --scope "agents/"`.
El comando genera un brief; no implementa la tarea ni prueba un AC por sí mismo.
Para preparar un contrato completo o comprobar su scope desde un baseline
explícito:

```sh
python -m agents.harness.task_runner tasks/us-d7-t4-grafana.jsonl --task-id US-D7-T4-00
python -m agents.harness.task_runner tasks/us-d7-t4-grafana.jsonl --task-id US-D7-T4-00 --baseline develop
```

El runner no ejecuta los comandos declarados ni modifica Git.

El readiness gate reúne las comprobaciones estructurales y, en modo normal,
las suites locales conocidas por el repositorio:

```sh
python -m agents doctor --static
python -m agents doctor
```

El modo estático sirve para CI cuando las suites se ejecutan en pasos separados.
Docker, Grafana y el backend no son requisitos de readiness del frontend.
Leer [AGENTS.md](../AGENTS.md), [arquitectura frontend](../docs/architecture.md) y
[guía](../docs/agentic-development.md) antes de editar.

Para uso cotidiano, basta entregar a Codex `Tarea`, `Resultado esperado` y
`Criterios de aceptación`. Codex prepara el contrato operativo antes de editar.
JSONL y los comandos siguientes son la interfaz avanzada para contratos
versionados y diagnóstico; las herramientas no invocan modelos ni implementan
por sí solas.
