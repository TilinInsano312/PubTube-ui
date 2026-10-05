# PubTube-Mod4-ui
Frontend PubTube Modulo 4 Para la asignatura de direccion de proyecto

PubTube-ui será el repositorio de la UI del Módulo 4. El stack acordado para
el frontend funcional es **Vue 3 + Vite**; todavía no está inicializado.
Grafana será la UI técnica de observabilidad, con Prometheus en infraestructura/backend.

## Desarrollo asistido por agentes

La fábrica en [agents/](agents/README.md) adapta la de PubTube-Mod4 a este repositorio.
Incluye estado del ciclo, perfiles, skills, orquestador, harness, plantillas y tests.
Consultar [AGENTS.md](AGENTS.md), la [guía de desarrollo](docs/agentic-development.md)
y el [formato de tareas JSONL](tasks/README.md).

Requisitos: Python 3.10 o posterior; pytest solo para ejecutar tests.
El código de la fábrica usa la biblioteca estándar, sin dependencias frontend.

```sh
python -m agents.harness.run_agent_loop "Preparar tarea UI" --ac "Alcance y evidencia definidos" --scope "agents/"
python -m compileall -q agents
python -m pytest -q agents/tests
```

Flujo Git: `main -> develop -> feature/*`. Preparar contrato, implementar,
validar, revisar diff y abrir PR hacia `develop`. El merge se autoriza por separado.
La fábrica se preparó sin inicializar el frontend funcional.

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

Grafana es diagnóstico técnico. Vue será la UI funcional del producto.
