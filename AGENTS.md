# PubTube-ui: instrucciones para agentes

PubTube-ui utiliza una fábrica agéntica para el frontend del Módulo 4.
El usuario y ChatGPT orquestan; Codex ejecuta, valida y reporta.
Leer la tarea actual, el estado real del repositorio, README, docs y contratos
antes de implementar. No asumir que archivos o servicios futuros ya existen.

## Ciclo y cierre

Aplicar `ANALYZE -> PLAN -> IMPLEMENT -> VERIFY -> REVIEW -> DECIDE`.
Usar cambios mínimos, sin refactors ni dependencias fuera de alcance.
Cada criterio de aceptación requiere evidencia concreta: comando o inspección,
resultado `PASS`, `FAIL` o `NOT VERIFIED`, y archivo/cambio asociado.
Revisar el diff completo, imports, regresiones, duplicación y secretos antes
de `DONE`. Un criterio obligatorio sin verificar impide `DONE`.
`CONTINUE` se reporta como `PARTIAL`; `BLOCKED` requiere una dependencia externa
o información necesaria que impida avanzar. No confundir dificultad con bloqueo.

## Git

Ejecutar `git status --short`, `git branch --show-current` y
`git log -1 --oneline` antes de editar. Identificar cambios previos y preservarlos.
Trabajar en ramas `feature/*` basadas en `develop`; nunca desarrollar directamente
sobre `main` ni `develop`. Verificar la base; ante una base incorrecta detenerse
y reportar, sin rebase ni merge automático. Usar Conventional Commits.
Revisar mediante PR hacia `develop`; el merge requiere autorización del orquestador.
No hacer force push ni borrar trabajo ajeno.

## Frontend

- Vue 3 + Vite es el stack acordado para la UI funcional futura.
- Mantener componentes pequeños; separar vistas, componentes, composables y servicios.
- Respetar contratos API reales; no hardcodear endpoints ni inventar contratos.
- Proteger secretos: las variables `VITE_*` son públicas en el navegador;
  nunca guardar tokens privados, passwords o credenciales en ellas.
- Cuando exista `package.json`, leer sus scripts y los lockfiles para identificar
  el gestor. Usar los scripts reales para lint, test, type-check y build.
  No inventar comandos ni asumir npm/pnpm/yarn.
- Si aún no existe frontend Vue, validar la fábrica Python; su ausencia no es
  un fallo npm. Esta tarea no autoriza inicializar Vue, Vite o `package.json`.

## Observabilidad y Docker

- Grafana es la UI técnica de observabilidad; no reimplementarlo mediante Vue.
- Versionar datasources, dashboards y provisioning reproducibles cuando una
  tarea futura lo autorice, usando contratos y métricas existentes.
- Prometheus pertenece a infraestructura/backend. El frontend consume métricas
  y servicios existentes, sin redefinir sus contratos ni inventar métricas.
- Evitar labels Prometheus de alta cardinalidad: usuario, email, títulos,
  eventId y correlationId.
- Inspeccionar configuración Docker existente; preservar redes, puertos y
  contratos. No añadir servicios de producto ni credenciales sin alcance explícito.

## Herramientas y documentación

Ver [guía operativa](docs/agentic-development.md), [ciclo](agents/software-engineering-loop.md)
y [plantilla de tarea](agents/templates/task-template.md).
Desde la raíz: `python -m agents.harness.run_agent_loop "Objetivo" --ac "Resultado verificable" --scope "agents/"`.
La fábrica prepara estado y briefs; el ejecutor realiza los cambios y registra
evidencia. No ejecuta automáticamente comandos, agentes externos ni merges.
Validación de la fábrica: `python -m compileall -q agents`,
`python -m pytest -q agents/tests`, `git diff --check` y revisión del diff.
Si pytest falta, usar un entorno local aislado; no cambiar dependencias del producto.
