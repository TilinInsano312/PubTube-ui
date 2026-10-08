# PubTube-Mod4-ui
Frontend PubTube Modulo 4 Para la asignatura de direccion de proyecto

PubTube-ui es el repositorio de la UI del Módulo 4. El frontend funcional está
inicializado con **Vue 3 + Vite + TypeScript**.
Grafana es la UI técnica de observabilidad, con Prometheus en infraestructura/backend.

## Desarrollar una tarea con Codex

No hace falta escribir JSONL para el trabajo cotidiano. Copia la
[plantilla breve](agents/templates/simple-task-template.md), completa sus tres
campos y envíala a Codex junto con esta instrucción:

> Ejecuta esta tarea siguiendo la fábrica agéntica del repositorio. Lee
> `AGENTS.md` antes de editar.

```text
Tarea: ...
Resultado esperado: ...
Criterios de aceptación:
- ...
```

Codex convierte esa solicitud en un contrato operativo, confirma el alcance,
implementa, valida y reporta `DONE`, `PARTIAL` o `BLOCKED`. Los contratos JSONL
quedan como formato avanzado para trabajo versionado con dependencias.

## Desarrollo del frontend

```sh
npm install
npm run dev
```

Para ejecutar las validaciones frontend vigentes:

```sh
npm run lint
npm run format:check
npm run test
npm run build
```

## Desarrollo asistido por agentes

La fábrica en [agents/](agents/README.md) adapta la de PubTube-Mod4 a este repositorio.
Incluye estado del ciclo, perfiles, skills, orquestador, harness, plantillas y tests.
Consultar [AGENTS.md](AGENTS.md), la [guía de desarrollo](docs/agentic-development.md),
el [Design System](docs/design-system.md) del frontend y el
[formato de tareas JSONL](tasks/README.md).
El estado y la trazabilidad de US-D5 están en
[docs/us-d5-status.md](docs/us-d5-status.md).

Requisitos: Python 3.10 o posterior; pytest solo para ejecutar tests.
El código de la fábrica usa la biblioteca estándar, sin dependencias frontend.

```sh
python -m agents doctor
python -m agents.contracts tasks/
python -m agents.harness.task_runner tasks/us-d7-t4-grafana.jsonl --task-id US-D7-T4-00
python -m agents.harness.run_agent_loop "Preparar tarea UI" --ac "Alcance y evidencia definidos" --scope "agents/"
python -m compileall -q agents
python -m pytest -q agents/tests
```

Estos comandos validan y preparan briefs; no invocan a Codex, no ejecutan los
comandos declarados en los contratos y no hacen merge.

Flujo Git: `main -> develop -> feature/*`. Preparar contrato, implementar,
validar, revisar diff y abrir PR hacia `develop`. El merge se autoriza por separado.
El frontend funcional está inicializado; sus features de producto evolucionan
únicamente según contratos y tareas autorizadas.

## Observabilidad técnica (US-D7-T4)

Grafana y el dashboard **PubTube Gateway** se provisionan desde archivos
versionados. Grafana utiliza el Prometheus existente de PubTube-Mod4/develop
por la red Docker `pubtube-network`; levantar el backend primero.
Ver [arranque, credenciales, paneles y reconstrucción](docs/grafana.md) y el
[contrato de siete pasos](tasks/us-d7-t4-grafana.jsonl).

```sh
# Con GRAFANA_ADMIN_PASSWORD definida en el entorno:
docker compose -f docker-compose.observability.yml up -d --wait
python scripts/observability/verify_grafana.py
```

Grafana es diagnóstico técnico. Vue es la UI funcional del producto.
