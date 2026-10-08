# PubTube-ui: instrucciones para agentes

PubTube-ui utiliza una fábrica agéntica para el frontend del Módulo 4.
El usuario y ChatGPT orquestan; Codex ejecuta, valida y reporta.
Leer la tarea actual, el estado real del repositorio, README, docs y contratos
antes de implementar. `docs/architecture.md` es obligatorio para cualquier
cambio del frontend. No asumir que archivos o servicios futuros ya existen.

## Documentación obligatoria

Antes de planificar o editar:

1. Leer `README.md` y `docs/architecture.md`.
2. Leer `docs/agentic-development.md` para el ciclo, harness y evidencia.
3. Leer el documento específico del alcance, por ejemplo `docs/grafana.md`, y
   el contrato de la tarea en `tasks/*.jsonl` cuando corresponda.
4. Contrastar esas decisiones con `package.json`, lockfiles y el código real.

Los documentos guían la implementación, pero no convierten una funcionalidad
planificada en una funcionalidad existente. Si hay una discrepancia entre docs,
contratos y código, registrarla y resolverla antes de inventar una solución.
Una modificación posterior de la arquitectura exige revisar las tareas y el
diff afectado.

## Ciclo y cierre

Aplicar `ANALYZE -> PLAN -> IMPLEMENT -> VERIFY -> REVIEW -> DECIDE`.
Antes de comenzar cada tarea, capturar `git rev-parse HEAD` y usar ese commit
como baseline exclusivo para validar su scope. En tareas secuenciales se captura
un baseline nuevo por tarea; no se reutiliza `develop` como baseline operativo.
Usar cambios mínimos, sin refactors ni dependencias fuera de alcance.
Cada criterio de aceptación requiere evidencia concreta: comando o inspección,
resultado `PASS`, `FAIL` o `NOT VERIFIED`, y archivo/cambio asociado.
Revisar el diff completo, imports, regresiones, duplicación y secretos antes
de `DONE`. Un criterio obligatorio sin verificar impide `DONE`.
`CONTINUE` se reporta como `PARTIAL`; `BLOCKED` requiere una dependencia externa
o información necesaria que impida avanzar. No confundir dificultad con bloqueo.

### Tareas humanas sin JSONL

Una solicitud válida con `Tarea`, `Resultado esperado` y `Criterios de
aceptación` es suficiente para el uso cotidiano. Antes de implementar, Codex
debe convertirla en un contrato operativo que explicite scope, acciones,
validaciones, restricciones y dependencias a partir de la solicitud y del estado
real del repositorio. Debe respetar ese scope, ejecutar evidencia aplicable y
cerrar como `DONE`, `PARTIAL` o `BLOCKED`.

JSONL sigue siendo la interfaz avanzada y versionable para planes con varias
tareas, dependencias o automatización. Ninguno de los comandos Python invoca a
Codex, ejecuta comandos arbitrarios del contrato ni autoriza un merge.

## Git

Ejecutar `git status --short`, `git branch --show-current` y
`git log -1 --oneline` antes de editar. Identificar cambios previos y preservarlos.
Trabajar en ramas `feature/*` basadas en `develop`; nunca desarrollar directamente
sobre `main` ni `develop`. Verificar la base; ante una base incorrecta detenerse
y reportar, sin rebase ni merge automático. Usar Conventional Commits.
Revisar mediante PR hacia `develop`; el merge requiere autorización del orquestador.
No hacer force push ni borrar trabajo ajeno.

## Frontend

- Vue 3 + Vite + TypeScript es el stack actual de la UI funcional.
- Mantener componentes pequeños; separar vistas, componentes, composables y servicios.
- Respetar contratos API reales; no hardcodear endpoints ni inventar contratos.
- Proteger secretos: las variables `VITE_*` son públicas en el navegador;
  nunca guardar tokens privados, passwords o credenciales en ellas.
- Cuando exista `package.json`, leer sus scripts y lockfiles para identificar el
  gestor. En este repositorio el gestor vigente es npm (`package-lock.json`).
  Usar los scripts reales para lint, test, type-check y build; no inventar
  comandos ni asumir dependencias que no estén instaladas.
- Si una capacidad frontend todavía no existe, distinguirla de lo planificado
  en `docs/architecture.md` y agregarla solo si la tarea la autoriza.

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

Ver [arquitectura frontend](docs/architecture.md), [guía operativa](docs/agentic-development.md),
[ciclo](agents/software-engineering-loop.md) y [plantilla de tarea](agents/templates/task-template.md).
Desde la raíz: `python -m agents.harness.run_agent_loop "Objetivo" --ac "Resultado verificable" --scope "agents/"`.
La fábrica prepara estado y briefs; el ejecutor realiza los cambios y registra
evidencia. No ejecuta automáticamente comandos, agentes externos ni merges.
Validación de la fábrica: `python -m compileall -q agents`,
`python -m pytest -q agents/tests`, `git diff --check` y revisión del diff.
Si pytest falta, usar un entorno local aislado; no cambiar dependencias del producto.
