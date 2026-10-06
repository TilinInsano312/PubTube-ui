# Desarrollo agéntico de PubTube-ui

La fábrica prepara desarrollo asistido por agentes del frontend del Módulo 4.
Vue 3 + Vite + TypeScript es el stack actual de la UI funcional. El frontend
base ya está inicializado; la fábrica no crea automáticamente nuevas features,
dashboards, Prometheus ni servicios Docker.
Grafana es la UI técnica de observabilidad; no debe reinventarse en Vue.

## Estructura y flujo

`AGENTS.md` contiene las reglas; `agents/core` representa estado/evidencia;
`profiles` especializa ingeniería, review, QA y documentación; `skills` define
capacidades; `orchestrator` asigna roles por fase; `harness` crea briefs y
descubre Markdown en `docs/`, incluidos ADR si existen. `templates` ofrece
contratos/reportes y `tests` verifica el ciclo sin servicios externos.

`ANALYZE -> PLAN -> IMPLEMENT -> VERIFY -> REVIEW -> DECIDE`

El usuario y ChatGPT orquestan; Codex ejecuta la tarea autorizada, registra
evidencia y reporta. La fábrica es un coordinador de estado determinista:
no llama modelos, no ejecuta shell automáticamente y no hace merges.

## Preparar y ejecutar una tarea

1. Verificar rama, base y cambios previos. Leer AGENTS, README y docs relevantes.
2. Usar la [plantilla](../agents/templates/task-template.md) para objetivo,
   scope, AC verificables, acciones, validaciones, riesgos y restricciones.
3. Generar el brief desde la raíz con Python 3.10 o posterior:

```sh
python -m agents.harness.run_agent_loop "Validar fabrica agentica UI" --ac "La fabrica puede generar un brief" --scope "agents/"
```

`--ac` y `--scope` pueden repetirse. `--project-root` selecciona el repositorio
para descubrir docs; `--no-docs` omite ese contexto. `--final-report` genera
un reporte inicial PARTIAL sin evidencia, nunca un cierre válido.
Exit code 0 significa que el brief/reporte se generó correctamente.
Leer documentos completos aplicables; sus extractos no sustituyen instrucciones.

4. Enviar contrato y brief a Codex indicando rama/base, restricciones y
   autorización de implementación, sin merge. Seguir el ciclo y registrar
   cada validación real. Seleccionar scripts únicamente si existen.
5. Revisar diff y completar el [reporte](../agents/templates/agent-report-template.md).

## API Python y cierre

```python
from agents import ChangeTrace, ValidationCheck, ValidationStatus
from agents.harness.run_agent_loop import build_agent_run

run = build_agent_run("Documentar la fabrica UI", ["Existe una guia operativa"], ["docs/"])
run.set_plan(["Inspeccionar", "Documentar", "Validar", "Revisar"])
# Después de editar y realizar la inspección indicada, registrar su evidencia real:
run.record_change(ChangeTrace("CHG-001", "AC1", "docs/agentic-development.md",
                             "Guia operativa", "revision de guia", ValidationStatus.PASS))
run.record_validation(ValidationCheck("revision de guia", ValidationStatus.PASS,
                                     "Guia inspeccionada con comandos reproducibles"))
run.record_review()  # Solo después de revisar el diff completo.
print(run.render_final_report(run.decide()))
```

El ejemplo enseña cómo registrar evidencia; no realiza una inspección automática.
`next_step(run)` identifica perfil/skill de la fase actual. Las llamadas
`set_plan`, `record_change`, `record_validation`, `record_review` y `decide`
actualizan las fases. Tests y reportes preservan decisiones, riesgos,
limitaciones y pendientes.

- **DONE**: AC explícitos con ChangeTrace PASS enlazado a un ValidationCheck
  PASS con evidencia, review vigente, sin checks fallidos/sin verificar,
  tests fallidos ni pendientes.
- **PARTIAL**: representación de CONTINUE; falta evidencia o trabajo ejecutable.
- **BLOCKED**: dependencia externa o información imprescindible impide avanzar;
  `decide(blocked_reason="motivo")` registra el pendiente.

La última entrada por AC/check es vigente; el historial anterior permanece en
el reporte. Tras corregir un fallo, repetir el check del mismo nombre; resolver
pendientes explícitamente. Una edición posterior invalida review. El ejecutor
debe repetir validaciones afectadas; el core no observa archivos ni garantiza
la veracidad de la evidencia aportada.

## Contratos JSONL

Consultar [tasks/README.md](../tasks/README.md) para campos, ejemplo y reglas.
Cada línea contiene una tarea completa con task_id, story, order, title,
objective, scope, actions, acceptance_criteria, validation, constraints,
dependencies y on_success. Preparar registros según estado real y comprobar
dependencias; trasladar objetivo/AC/scope al CLI y el resto al prompt de Codex.
El harness no ejecuta JSONL ni acciones automáticamente. US-D7-T4 se contratará
por separado; el ejemplo documentado solo comprueba generación de un brief.

## Git y validación

```text
main
└── develop
    └── feature/*
```

Proceso: **contrato -> implementación -> validación -> review -> PR -> merge**.
Crear feature desde develop, verificar base y no trabajar directamente en main
ni develop. Preservar cambios ajenos, Conventional Commits, sin force push.
Abrir PR hacia develop; merge solo autorizado por el orquestador.

El runtime usa biblioteca estándar. Para tests, crear entorno local y activar:

```sh
python -m venv .venv
# POSIX: . .venv/bin/activate
# PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install pytest
python -m compileall -q agents
python -m pytest -q agents/tests
git diff --check
git status --short
git diff --stat
git diff
```

Si no puede activarse, usar directamente `.venv/bin/python` en POSIX o
`.\.venv\Scripts\python.exe` en Windows. Pytest es herramienta de validación
aislada, no dependencia del producto. Si no está disponible, informar
NOT VERIFIED; no ocultar el fallo.

Cuando exista package.json, inspeccionar scripts, lockfile y gestor antes de
lint, test, type-check o build. En este repositorio se usa npm y la validación
frontend disponible es `npm run build`; no inventar scripts que no existan.
Proteger secretos: VITE_* es público, endpoints configurados mediante mecanismos
existentes y contratos API conservados. Grafana usa datasources/dashboards/
provisioning versionados cuando estén autorizados; Prometheus sigue en backend,
sin métricas inventadas ni labels de alta cardinalidad. Inspeccionar Docker
existente y diferenciar validación estática de evidencia runtime.
