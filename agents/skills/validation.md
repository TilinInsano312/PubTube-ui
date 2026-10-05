# Skill: Validation (`validation`)

Producir evidencia por AC. Elegir comandos por el estado real del repositorio.
Si existe package.json, leer scripts y lockfiles e identificar npm/pnpm/yarn;
usar únicamente scripts existentes para lint, test, type-check y build.
Registrar como no disponible cualquier comprobación requerida sin script.
No añadir scripts o dependencias del producto para ocultar esa ausencia.

Si no existe frontend Vue, ejecutar desde la raíz:

```sh
python -m compileall -q agents
python -m pytest -q agents/tests
python -m agents.harness.run_agent_loop "Validar fabrica agentica UI" --ac "La fabrica puede generar un brief" --scope "agents/"
git diff --check
```

Usar un entorno aislado si pytest falta; si realmente no puede ejecutarse,
informar NOT VERIFIED y la causa. La ausencia de npm no invalida la fábrica.
Docker/Grafana requieren configuración existente; diferenciar validación de
configuración de comprobaciones runtime. No inventar métricas para las pruebas.
Salida: nombre de check, PASS/FAIL/NOT VERIFIED, evidencia y conteos reales.
