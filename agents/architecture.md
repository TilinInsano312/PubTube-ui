# Arquitectura de la fábrica UI

La referencia inspeccionada es PubTube-Mod4/develop, commit
`46a115c372403b395dcc639ba0b2c8b9c6aad0e4`.
Se conservan las estructuras y API Python del backend, imports públicos,
descubrimiento de Markdown/ADR, CLI, catálogos extensibles y reportes.
Las instrucciones operativas se adaptan a Vue/Vite y observabilidad técnica.

| Área | Responsabilidad |
| --- | --- |
| `core/` | Fases, decisiones, AC, ChangeTrace, ValidationCheck, TestSummary y AgentRun. |
| `profiles/` | Responsabilidades especializadas del frontend. |
| `skills/` | Capacidades por fase con evidencia esperada. |
| `orchestrator/` | Asignación determinista de fase a perfil y skill. |
| `harness/` | Numerar AC, recibir scope, descubrir docs, generar brief y reporte. |
| `templates/` | Contrato de tarea y reporte manual. |
| `tests/` | Core, documentos, CLI y ciclo completo sin red. |

| Fase | Perfil | Skill |
| --- | --- | --- |
| ANALYZE | software_engineer | repository_inspection |
| PLAN | software_engineer | repository_inspection |
| IMPLEMENT | software_engineer | implementation |
| VERIFY | qa_validator | validation |
| REVIEW | reviewer | diff_review |
| DECIDE | documentation_curator | reporting |

`next_step(run)` devuelve la asignación de la fase actual; el ejecutor cambia
el estado mediante métodos de AgentRun. El orquestador no llama modelos ni
ejecuta shell. `agentic_loop.py` conserva imports de compatibilidad.

Extender perfiles/skills en sus catálogos y Markdown; modificar asignaciones
en el orquestador. Mantener cada asignación compatible con las fases de la skill.
Se añade `diff-review.md` para documentar la quinta skill ya presente en el backend;
`tasks/README.md` versiona y explica contratos, y `.gitignore` excluye artefactos Python.

Mejoras de cierre respecto de la referencia: exigir AC explícitos, evidencia
de un check PASS enlazado, review y ausencia de tests fallidos o checks sin
verificar. La última evidencia por AC/check permite corregir una validación
fallida sin perder su historial. Una edición posterior invalida la review.
Los hallazgos de review son pendientes hasta su resolución explícita.
