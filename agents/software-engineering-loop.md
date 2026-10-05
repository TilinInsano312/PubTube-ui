# Ciclo de ingeniería PubTube-ui

Fuente de verdad: tarea actual, estado real, documentación vigente, tests,
arquitectura y convenciones existentes, supuestos mínimos. Leer ADR si existen;
no trasladar decisiones del backend sin comprobar su aplicabilidad al frontend.

`ANALYZE -> PLAN -> IMPLEMENT -> VERIFY -> REVIEW -> DECIDE`

1. **ANALYZE**: verificar rama/base y cambios previos; identificar objetivo,
   scope, AC, riesgos y archivos existentes según repository-inspection.
2. **PLAN**: definir 3 a 7 pasos verificables y comandos reales.
3. **IMPLEMENT**: cambio mínimo en el área autorizada. Vue 3/Vite cuando esté
   inicializado; separar componentes, vistas, composables y servicios API.
   No hardcodear endpoints ni exponer secretos en `VITE_*`.
4. **VERIFY**: registrar comando/inspección, resultado y evidencia por AC.
   Validar Python si no hay frontend; inspeccionar scripts/lockfiles si lo hay.
5. **REVIEW**: revisar diff completo, secretos, imports, duplicación,
   acoplamiento, regresiones, dependencias y contratos. Resolver hallazgos.
6. **DECIDE**: `DONE` solo con todos los AC verificados, review y validaciones
   relevantes completas. `CONTINUE` para trabajo pendiente; reportarlo `PARTIAL`.
   `BLOCKED` ante dependencia externa imprescindible, con motivo y siguiente acción.

Si una validación falla: registrar observado/esperado, formular una hipótesis,
corregir y repetir el check mínimo. Conservar la evidencia previa; una nueva
validación del mismo nombre sustituye su resultado vigente. No alterar tests
para ocultar fallos. Una nueva edición requiere nueva review y, si corresponde,
nueva validación. El ejecutor responde de la vigencia de la evidencia.

Grafana es UI técnica, nunca una réplica Vue. Prometheus pertenece a
infraestructura/backend; consumir contratos existentes, sin inventar métricas
ni labels de alta cardinalidad. Versionar provisioning autorizado y preservar
configuración Docker existente, sin añadir servicios fuera de alcance.

Trazabilidad: `AC1 -> CHG-001 -> archivo -> validación -> PASS/FAIL/NOT VERIFIED`.
Usar [plantilla de tarea](templates/task-template.md) y
[reporte](templates/agent-report-template.md). Proteger secretos también en
logs y reportes. No hacer merge hasta autorización del orquestador.
