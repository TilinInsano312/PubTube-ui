# Contratos de tareas Codex

JSONL es la interfaz avanzada para planes versionados, dependencias y
automatización. Para una tarea cotidiana no es obligatorio: se puede entregar a
Codex la [plantilla humana breve](../agents/templates/simple-task-template.md)
con `Tarea`, `Resultado esperado` y `Criterios de aceptación`. Codex prepara el
contrato operativo antes de implementar según `AGENTS.md`.

Este directorio queda versionado mediante esta documentación. Una tarea puede
representarse en un archivo UTF-8 `.jsonl`: un objeto JSON por línea, sin array
envolvente, comentarios ni saltos de línea dentro de cada objeto.
El contrato [us-d7-t4-grafana.jsonl](us-d7-t4-grafana.jsonl) prepara e implementa
Grafana en siete registros ordenados; requiere evidencia runtime para DONE.

La referencia de formato inspeccionada es
`PubTube-Mod4/tasks/us-d7-t2-ci-runtime-smoke.jsonl`, commit
`46a115c372403b395dcc639ba0b2c8b9c6aad0e4`; aquí se adapta la estructura,
sin copiar acciones, contratos ni comandos de producto del backend.

| Campo | Tipo / significado |
| --- | --- |
| task_id | String único por registro. |
| story | String de historia o agrupación. |
| order | Entero no negativo, orden propuesto dentro de la historia. |
| title | String, título breve. |
| objective | String, resultado concreto. |
| scope | Lista de rutas/áreas autorizadas. |
| actions | Lista de pasos ejecutables. |
| acceptance_criteria | Lista de resultados verificables, numerados AC1… por ejecución. |
| validation | Lista de objetos id/type/command/expected; comandos reales o inspecciones. |
| constraints | Lista de restricciones y protección de secretos. |
| dependencies | Lista de task_id previos; vacía si no existen. |
| final_report_schema | Objeto JSON opcional que define el reporte final esperado; el task runner lo conserva y muestra en el brief. |
| on_success | CONTINUE para siguiente registro; DONE para cerrar tras evidencia. |

Los campos no documentados se rechazan con un error de esquema que incluye el
archivo y la línea. Esto evita que una errata o una extensión contractual se
ignore silenciosamente. Los objetos de `validation` aceptan únicamente `id`,
`type`, `command` y `expected`.

Ejemplo ilustrativo exclusivo de la fábrica (no representa US-D7-T4):

```jsonl
{"task_id":"EXAMPLE-UI-FACTORY-001","story":"EXAMPLE","order":0,"title":"Preparar brief","objective":"Generar un brief de la fábrica UI","scope":["agents/"],"actions":["Leer AGENTS.md","Ejecutar el harness desde la raíz","Inspeccionar el brief"],"acceptance_criteria":["El brief incluye AC1, scope y perfil asignado"],"validation":[{"id":"V1","type":"command","command":"python -m agents.harness.run_agent_loop \"Ejemplo de fabrica UI\" --ac \"El brief incluye AC1\" --scope \"agents/\"","expected":"Exit code 0 y Agent Run Brief con AC1"}],"constraints":["No inicializar Vue ni implementar Grafana","No hacer merge"],"dependencies":[],"on_success":"DONE"}
```

El orquestador humano valida unicidad, dependencias existentes/sin ciclos y
orden antes de enviar registros a Codex. El validador reproducible realiza esa
comprobación para un archivo o para todos los `.jsonl` de un directorio:

```sh
python -m agents.contracts tasks/
python -m agents.contracts tasks/us-d7-t4-grafana.jsonl
```

El comando valida JSON, esquema, IDs y el grafo de dependencias. Trata los
campos `command` e `inspection` únicamente como datos: nunca los ejecuta.
`on_success` no autoriza merge ni publicación. El harness de briefs se invoca
por separado y tampoco programa dependencias ni ejecuta comandos arbitrarios.
