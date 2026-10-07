# Arquitectura Frontend de PubTube UI

## Objetivo y estado actual

Este documento define los límites y las decisiones de arquitectura para la UI
funcional del Módulo 4. Debe leerse junto con `AGENTS.md`, el README y la tarea
que se esté ejecutando.

El frontend Vue ya está inicializado y contiene la primera feature de
producto (`src/features/auth`: vistas de login y registro con Vue Router).
Todavía no existen integración HTTP ni estado global. Por eso este documento
separa explícitamente lo que existe de lo que queda planificado:

- **Implementado:** Vue 3, Vite, TypeScript, Composition API, `<script setup>`,
  scripts npm `dev`, `build` y `preview`, Vue Router con las rutas `/login` y
  `/register`, y la feature de autenticación en `src/features/auth`.
- **Implementado fuera de Vue:** provisioning de Grafana y su compose de
  observabilidad; Grafana es la UI técnica y consume Prometheus del backend.
- **Planificado:** cliente API, Pinia, estilos/componentes adicionales y
  pruebas frontend.
- **No disponible en este repositorio:** el backend, sus endpoints efectivos,
  RabbitMQ, PostgreSQL y los contratos funcionales completos. No deben
  inventarse para avanzar una pantalla.

## Stack y herramientas

### Stack vigente

| Área | Tecnología | Estado |
| --- | --- | --- |
| UI | Vue 3 | Instalada en `package.json` |
| Build/dev server | Vite | Instalado y validado con `npm run build` |
| Lenguaje | TypeScript | Configurado con `vue-tsc` |
| Routing | Vue Router | Instalado en `package.json`; rutas `/login` y `/register` |
| Estilo de componentes | Composition API y `<script setup>` | Usado por el scaffold |
| Gestor | npm | Confirmado por `package-lock.json` |
| Validación actual | `vue-tsc -b` + `vite build` | Script `npm run build` |

### Dependencias que todavía no forman parte del proyecto

Pinia, Tailwind CSS, Lucide Vue, Axios, Vitest, Playwright,
ESLint y Prettier no están instalados actualmente. Solo deben incorporarse
cuando una tarea concreta los necesite, con justificación y actualización del
lockfile. La arquitectura no autoriza asumir que esas herramientas ya existen.

## Límites del repositorio

```text
.
├── src/                         # Aplicación Vue funcional
├── public/                      # Assets públicos del frontend
├── docs/                        # Arquitectura, operación y observabilidad
├── agents/                      # Harness y orquestador del repositorio
├── observability/grafana/       # Dashboards y provisioning técnico
├── tasks/                       # Contratos de trabajo JSONL
└── docker-compose.observability.yml
```

La UI funcional vive en `src/`. La automatización de agentes, la documentación
y Grafana tienen responsabilidades distintas y no deben mezclarse con
componentes de producto.

`App.vue` muestra el `RouterView` y `main.ts` monta la aplicación con el
router. El componente de ejemplo de Vite se eliminó al iniciar la primera
feature real; no se deben crear capas vacías solo para completar una
estructura ideal.

## Estructura objetivo de `src/`

Esta es una guía para cuando existan features reales; los directorios no deben
crearse anticipadamente sin una necesidad concreta.

```text
src/
├── api/                         # Cliente HTTP y funciones por contrato
├── features/                    # Funcionalidad específica del producto
│   └── auth/                    # Vistas, componentes, composables y tipos de login/registro
├── layouts/                     # Composición compartida de páginas
├── router/                      # Rutas reales (login y register)
├── stores/                      # Estado compartido que justifique Pinia
├── shared/
│   ├── ui/                      # Primitives sin conocimiento de una feature
│   ├── composables/
│   ├── types/
│   └── utils/
├── App.vue
└── main.ts
```

### `api/`

Será el único punto de integración HTTP de la UI. Se prioriza `fetch` mediante
un wrapper pequeño y tipado. Las funciones `*.api.ts` deben reflejar endpoints
que existan en el contrato real del backend; no deben contener componentes ni
estado visual, ni inventar rutas, payloads o respuestas.

### `features/`

Cada feature puede contener sus vistas, componentes, composables y tipos
específicos. No se crearán capas `domain`, `repositories` o `use-cases` salvo
que una necesidad demostrable justifique esa complejidad.

### `shared/`

Solo contiene elementos realmente reutilizables y sin conocimiento de una
feature. Un componente que conoce el dominio de publicaciones o notificaciones
pertenece a su feature, no a `shared/ui`.

### `stores/`, router y layouts

El estado local debe permanecer en el componente o composable. Pinia solo se
agregará para sesión, wizards que crucen rutas u otro estado compartido real.
Vue Router ya está incorporado con la feature de autenticación (`/login` y
`/register`); los layouts compartidos se agregarán cuando más de una feature
necesite la misma composición de página.

## Flujo de datos

Cuando la funcionalidad esté disponible, el flujo esperado será:

```text
Vista / componente
        ↓
Composable o store, solo si aporta valor
        ↓
Funciones de api/*.api.ts
        ↓
Cliente HTTP compartido
        ↓
Backend del sistema
```

El scaffold actual todavía no implementa este flujo. Las decisiones de
autenticación, errores, polling o actualización en tiempo real deben basarse
en el contrato del backend correspondiente.

## Integración y contratos

El backend se mantiene fuera de este repositorio. Antes de crear una llamada
o una vista, se debe localizar el contrato vigente en la tarea, documentación
o repositorio backend autorizado. Si no existe evidencia del endpoint o del
modelo, la implementación queda pendiente y se reporta la ambigüedad.

No se implementarán WebSockets, SSE, polling, autenticación ni rutas de negocio
por anticipación. Se usarán únicamente cuando una tarea y un contrato real los
autoricen. Las variables `VITE_*` son públicas en el navegador y nunca deben
contener secretos, contraseñas, tokens privados o credenciales.

## Observabilidad y Grafana

Grafana es la UI técnica de observabilidad y no debe reimplementarse dentro de
Vue ni incrustarse como sustituto de la UI funcional. Este repositorio versiona
su provisioning en `observability/grafana/` y lo levanta con
`docker-compose.observability.yml` sobre la red externa `pubtube-network`.

Prometheus y las métricas pertenecen al backend/infraestructura. La UI puede
consumir contratos o endpoints existentes cuando una tarea lo autorice, pero
no debe redefinir métricas, crear exporters ni usar `correlationId`, `eventId`,
usuarios, correos o títulos como labels Prometheus.

## Calidad y validación

Los comandos deben salir de los scripts reales de `package.json`:

```sh
npm install
npm run build
```

`npm run build` ejecuta el type-check de `vue-tsc` y el build de Vite. No hay
scripts frontend de lint o tests configurados todavía; no se deben declarar
como evidencia hasta que una tarea los agregue. La fábrica Python se valida de
forma independiente con:

```sh
python -m compileall -q agents
python -m pytest -q agents/tests
```

## Fuentes de verdad y conflictos

- `AGENTS.md`: reglas operativas obligatorias para agentes.
- `docs/architecture.md`: límites y decisiones de arquitectura frontend.
- `docs/agentic-development.md`: ciclo, harness, orquestador y evidencia.
- `docs/grafana.md`: operación de la observabilidad técnica.
- `tasks/*.jsonl`: alcance, criterios y validaciones de cada tarea.
- Contratos y documentación del backend autorizado: integración HTTP real.
- Código y lockfiles: estado efectivo de dependencias y scripts.

Si dos fuentes discrepan, no se debe elegir silenciosamente. Se debe señalar
la discrepancia, confirmar la fuente vigente y actualizar la documentación o
el código dentro del alcance autorizado.

## Principio general

Preferir la solución más pequeña que cumpla el requisito, sea legible y pueda
mantenerse. La escalabilidad debe surgir de límites claros entre features,
componentes, composables y servicios, no de capas preventivas sin consumidor.
