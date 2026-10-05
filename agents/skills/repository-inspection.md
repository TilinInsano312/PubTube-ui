# Skill: Repository Inspection (`repository_inspection`)

Fases ANALYZE y PLAN. Leer tarea, preflight Git, rama/base, cambios previos
y archivos relevantes que realmente existan:

- `README.md`, `AGENTS.md`, `docs/` y `docs/adr/`.
- `tasks/` y contratos aplicables.
- `package.json`, lockfiles y `vite.config.*`.
- `src/`, vistas, componentes, composables, servicios y `tests/`.
- `docker-compose*`, `observability/` y `grafana/`.

Nunca asumir que estas rutas o el frontend ya existen. Buscar primero los
archivos y luego símbolos, imports y contratos. El harness descubre Markdown
de docs salvo `--no-docs`; el ejecutor lee el contenido relevante completo.
Salida: TASK, SCOPE, AC, RISKS y plan de pasos verificables.
