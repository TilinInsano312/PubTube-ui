# Skill: Minimal Implementation (`implementation`)

Aplicar el cambio mínimo que cumple el contrato. No refactors ajenos,
dependencias sin justificación ni ediciones fuera de scope.
En Vue separar vistas/componentes/composables/servicios y evitar acoplamiento.
Configurar endpoints con mecanismos existentes; `VITE_*` es público.
Preservar contratos reales; Grafana usa provisioning versionado cuando se
autorice y Prometheus permanece en infraestructura/backend.

Salida: diff acotado y ChangeTrace por AC con validación asociada.
