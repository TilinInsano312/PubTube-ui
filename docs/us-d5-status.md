# Estado de US-D5

Este documento mantiene la trazabilidad del dashboard de publicaciones en
PubTube UI. Distingue el código ya mergeado de las Issues de GitHub que aún
requieren una acción administrativa. La matriz se actualiza contra `develop` y
no convierte una referencia planificada en un contrato disponible.

## Matriz de implementación

| Issue | Alcance | Estado técnico | PR mergeada en `develop` | Evidencia principal |
| --- | --- | --- | --- | --- |
| #6 | Componentes UI reutilizables | Implementada | [#14](https://github.com/TilinInsano312/PubTube-ui/pull/14) · `207be92` | Build final PASS |
| #7 | Shell de aplicación responsive | Implementada | [#15](https://github.com/TilinInsano312/PubTube-ui/pull/15) · `33df880` | Build final PASS |
| #8 | Filtros del dashboard y KPIs | Implementada | [#16](https://github.com/TilinInsano312/PubTube-ui/pull/16) · `68f4118` | Build final PASS |
| #9 | Cliente de counts de dashboard | Implementada | [#17](https://github.com/TilinInsano312/PubTube-ui/pull/17) · `1da910d` | Build final PASS; contrato limitado a `GET /api/dashboard` |
| #10 | Tabla de publicaciones y estados visuales | Implementada | [#18](https://github.com/TilinInsano312/PubTube-ui/pull/18) · `296aa8a` | Build final PASS; sin filas mock productivas |
| #11 | Composición responsive del dashboard | Implementada | [#19](https://github.com/TilinInsano312/PubTube-ui/pull/19) · `09b3e53` | Build final PASS |
| #12 | Fuente real para detalle individual | **Bloqueada** | Sin PR | Falta contrato backend verificable |
| #13 | Accesibilidad, estados y Design System | Implementada | [#20](https://github.com/TilinInsano312/PubTube-ui/pull/20) · `d52fb87` | Build, revisión de contraste y auditoría PASS |

La Issue [#5](https://github.com/TilinInsano312/PubTube-ui/issues/5) es el
tracking de US-D5. Las unidades implementables (#6–#11 y #13) están mergeadas;
el detalle individual permanece separado en la #12 porque depende de un
contrato backend que todavía no está disponible.

## Validación acumulada en `develop`

Los siguientes checks se ejecutaron sobre el estado integrado antes de esta
documentación:

| Check | Resultado | Evidencia |
| --- | --- | --- |
| Build frontend | PASS | `npm.cmd run build` |
| Fábrica Python: compilación | PASS | `python -m compileall -q agents` |
| Fábrica Python: tests | PASS | `python -m pytest -q agents/tests` · 23 tests |
| Integridad del diff | PASS | `git diff --check` |
| Runtime de `GET /api/dashboard` | NOT VERIFIED | No había backend local disponible |
| Inspección visual interactiva contra Figma | NOT VERIFIED | No se contó con una sesión visual verificable |

La ausencia de runtime del backend no se oculta con fixtures: la UI conserva
los estados de carga, vacío y error sin inventar publicaciones.

## Verificación de la Issue #12

La #12 **no es implementable todavía** de forma segura. La evidencia
inspeccionada en `PubTube-Mod4` sobre `origin/develop` (`13fcaec`) muestra que
el gateway solo expone para Module 3:

- `POST /publish/schedule`;
- `POST /publish/{publication_id}/now`;
- `GET /publish/{publication_id}/status`.

Ninguna de esas rutas entrega un listado o un detalle con el contrato que
necesita `PublicationTable`. Además, la mención a `GET /api/dashboard` en
`PubTube-Mod4/docs/observability-plan-v01.md` es parte de un plan de
observabilidad, no evidencia de una ruta implementada ni de un schema de
respuesta.

Para desbloquear la #12 el backend debe aportar evidencia verificable de:

- endpoint y método;
- schema de respuesta, con `id` estable, `contentId` o identificador
  presentable, `state` y `scheduleAt` por publicación;
- relación entre publicación y contenido;
- filtros, paginación, ordenamiento y zona horaria;
- errores HTTP y su forma de respuesta.

El título/contenido visual es opcional para el mínimo de la tabla. Hasta que
esa evidencia exista, no se debe inventar endpoint, payload, mock productivo,
thumbnail, attempts ni `lastError`.

## Estado administrativo de GitHub

La documentación quedó integrada en `develop` mediante la PR #21. La #5 y las
Issues #6–#11 y #13 están cerradas con sus PR correspondientes. La #12 sigue
abierta y etiquetada como `BLOCKED` hasta que aparezca el contrato backend.
