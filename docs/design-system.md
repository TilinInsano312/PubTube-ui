# Design System de PubTube UI

Este documento define las **reglas base de diseño, interacción y consistencia visual** de la interfaz funcional de PubTube UI.

Su propósito es mantener un criterio común aunque cambien la implementación, los componentes, las dependencias o los valores concretos del código. Por ello, este documento define **intención, semántica y restricciones**; los valores visuales efectivos y los detalles de implementación pertenecen al código.

## 1. Convenciones normativas

En este documento:

- **DEBE / NO DEBE** indica una regla obligatoria.
- **DEBERÍA / NO DEBERÍA** indica la opción preferida salvo una razón explícita para apartarse de ella.
- **PUEDE** indica una opción válida dependiente del contexto.

Una excepción a una regla obligatoria debe estar justificada por una necesidad concreta del producto y no por preferencia visual local.

---

## 2. Alcance

Este Design System regula:

- identidad y dirección visual;
- semántica y uso de tokens;
- tipografía;
- espaciado, forma, elevación y movimiento;
- densidad de interfaz;
- layout de escritorio;
- navegación principal;
- jerarquía de acciones;
- estados de interfaz y feedback;
- formularios y validación desde el punto de vista de UX;
- tablas y listados de datos;
- accesibilidad;
- iconografía;
- contenido y microcopy;
- criterios para reutilizar o extender soluciones visuales.

No regula:

- arquitectura de carpetas o dependencias internas;
- integración HTTP ni contratos de backend;
- estado global, routing o flujo de datos;
- Git, CI, agentes o proceso de desarrollo;
- Grafana u observabilidad técnica;
- APIs concretas de componentes;
- valores exactos que ya tengan una fuente de verdad en código.

Consultar también:

- [`architecture.md`](./architecture.md): arquitectura y límites del frontend;
- [`agentic-development.md`](./agentic-development.md): flujo de desarrollo y validación;
- [`grafana.md`](./grafana.md): observabilidad técnica.

---

## 3. Fuentes de verdad

La información no debe duplicarse entre documentación y código.

| Responsabilidad | Fuente de verdad |
| --- | --- |
| Reglas y significado del sistema visual | `docs/design-system.md` |
| Valores visuales concretos | `src/styles/tokens.css` |
| Estilos globales efectivos | `src/styles/global.css` |
| Implementación y API de UI existente | código fuente |
| Arquitectura y responsabilidades | `docs/architecture.md` |
| Dependencias instaladas | `package.json` y lockfile |

### 3.1 No duplicación

Este documento **NO DEBE** copiar:

- valores hexadecimales;
- tamaños exactos de fuentes, espacios, radios o controles;
- sombras completas;
- `z-index` concretos;
- duraciones de animación;
- CSS de implementación;
- props o tipos definidos en TypeScript;
- dependencias que puedan verificarse en `package.json`.

Puede definir categorías, semántica, relaciones y reglas de uso.

### 3.2 Conflictos

Si código y documentación discrepan:

1. no se elige silenciosamente una de las dos fuentes;
2. se determina si cambió la intención de diseño o solo la implementación;
3. se corrige la fuente correspondiente;
4. este documento solo se modifica cuando cambia una regla conceptual o semántica.

---

## 4. Dirección visual

PubTube UI es una **herramienta operativa de escritorio** para gestionar y supervisar un flujo editorial. La interfaz DEBE priorizar lectura rápida, estado del sistema, acciones claras y densidad útil por sobre decoración.

La dirección visual es:

- profesional y sobria;
- propia de un dashboard/SaaS de gestión;
- predominantemente clara (`light`);
- basada en una familia morada para marca, interacción y acción;
- apoyada por neutros para superficies, texto y bordes;
- con familias semánticas independientes para información, éxito, advertencia y peligro;
- con azul reservado para información, no para branding;
- con ornamentación contenida y jerarquía visual explícita.

La interfaz NO DEBE imitar visualmente YouTube ni depender de su lenguaje gráfico.

### 4.1 Tema

El producto soporta **únicamente tema claro**.

No se deben crear estilos, variantes o complejidad preventiva para dark mode mientras no exista un requisito explícito.

---

## 5. Principios base

### 5.1 Consistencia antes que novedad

Antes de introducir un patrón visual, token o solución nueva, DEBE revisarse si el repositorio ya contiene una alternativa equivalente y reutilizable.

### 5.2 Semántica antes que apariencia

La UI DEBE expresar conceptos como `text`, `surface`, `border`, `action`, `success`, `warning` o `danger`, evitando acoplar el significado a un valor visual concreto.

### 5.3 Marca y estado son conceptos distintos

El color de marca representa principalmente navegación, selección, foco, acción o énfasis del producto. NO DEBE usarse como sustituto genérico de éxito, advertencia o error.

### 5.4 Accesibilidad por defecto

La accesibilidad forma parte de la definición de una solución visual, no es una mejora posterior.

### 5.5 Densidad controlada

PubTube utiliza una **densidad compacta moderada**: debe aprovechar el espacio de escritorio sin convertirse en una interfaz comprimida tipo IDE.

Se prioriza:

- mayor densidad dentro de tablas, filtros y toolbars;
- mayor separación entre secciones y grupos funcionales;
- controles legibles y áreas de interacción consistentes;
- jerarquía clara aun cuando exista mucha información.

### 5.6 Abstracción solo cuando aporta valor

No se crean tokens, variantes ni soluciones genéricas para necesidades hipotéticas. La generalización debe responder a una necesidad estable o repetida.

### 5.7 Automatizar lo verificable

Si una regla puede comprobarse de manera fiable mediante tipos, linting, tests o tooling, DEBERÍA automatizarse. Este documento conserva la intención; no reemplaza controles técnicos.

---

## 6. Tokens de diseño

Los valores visuales globales DEBEN centralizarse en:

```text
src/styles/tokens.css
```

Los estilos globales que consumen esos tokens DEBEN residir en:

```text
src/styles/global.css
```

### 6.1 Niveles

El sistema utiliza dos niveles principales.

#### Tokens primitivos

Definen escalas visuales sin significado funcional, por ejemplo:

```text
color.primary.*
color.ink
color.muted
color.border.*
color.canvas
color.surface.*
color.info.*
color.success.*
color.warning.*
color.danger.*
space.*
radius.*
shadow.*
font.*
motion.*
size.*
z.*
```

#### Tokens semánticos

Definen intención de uso, por ejemplo:

```text
color.text.primary
color.text.secondary
color.text.inverse
color.background.canvas
color.background.surface
color.background.sunken
color.border.default
color.border.strong
color.action.primary
color.action.primary-hover
color.action.primary-active
color.action.primary-soft
color.action.primary-soft-strong
color.status.success.solid
color.status.success.soft
color.status.success.text
color.status.warning.solid
color.status.warning.soft
color.status.warning.text
color.status.danger.solid
color.status.danger.soft
color.status.danger.text
color.status.info.solid
color.status.info.soft
color.status.info.text
color.focus
color.selection
```

La nomenclatura exacta puede evolucionar, pero DEBE conservar una estructura basada en **categoría + intención + estado**, nunca en el valor actual.

### 6.2 Reutilización semántica

Antes de crear un token semántico nuevo se DEBE:

1. comprobar si ya existe un concepto equivalente;
2. reutilizar el token existente cuando el significado sea el mismo;
3. si se necesita un nuevo nombre por claridad semántica, preferir un alias que apunte a un valor o token existente antes que introducir un color nuevo;
4. crear un valor visual nuevo solo cuando exista una diferencia real de significado o jerarquía.

Dos nombres diferentes NO DEBEN generar colores diferentes si representan la misma intención.

### 6.3 Catálogo de foundations

`src/styles/tokens.css` es el catálogo exacto de valores. La API recomendada
para consumers se organiza en estas foundations:

- **Color:** `primary-50..900`, `ink`, `muted`, `border`, `border-strong`,
  `canvas`, `surface`, `surface-sunken`, y las familias semánticas
  `info`, `success`, `warning` y `danger`.
- **Tipografía:** familia sans y mono, pesos, y los roles `display`,
  `heading-1`, `heading-2`, `heading-3`, `body`, `small`, `caption` y `mono`.
- **Spacing:** la escala `space-1` a `space-16` con los pasos aprobados.
- **Forma y controles:** `radius-*`, `control-height-*`, `icon-size-*`,
  `border-width-default` y el focus ring.
- **Elevación y movimiento:** `shadow-*`, `motion-duration-*` y
  `motion-easing-standard`.
- **Layout:** `layout-navigation-rail-width`, `layout-topbar-height` y
  `layout-dashboard-width`.

Los valores concretos no se duplican aquí: cualquier cambio aprobado debe
actualizar primero el CSS y después esta descripción semántica si cambia la
API. No existe una paleta primaria azul paralela.

### 6.4 Valores arbitrarios

No se deben introducir valores locales arbitrarios para:

- color;
- tipografía;
- espaciado recurrente;
- radios;
- sombras;
- alturas estándar de controles;
- `z-index` del sistema;
- motion.

Una necesidad estructural específica de layout puede utilizar un valor local cuando convertirlo en token no aporte reutilización ni significado.

---

## 7. Color

La paleta efectiva se define en código.

Debe existir cobertura semántica para:

- marca / acción;
- texto principal, secundario y atenuado;
- superficie de página, superficie principal y superficie secundaria;
- bordes normales y enfatizados;
- foco;
- éxito;
- advertencia;
- peligro / error;
- información.

### Reglas

- El color NO DEBE ser el único mecanismo para transmitir un estado.
- Un estado importante DEBE reforzarse con texto, iconografía, forma o etiqueta según corresponda.
- El color primario NO DEBE sustituir estados semánticos.
- Los estados del dominio DEBEN mapearse a la semántica visual existente antes de crear nuevas familias de color.
- La aparición de un nuevo estado del backend NO implica automáticamente un nuevo token de color.
- Los valores efectivos DEBEN cumplir los requisitos de contraste definidos en accesibilidad.

| Semántica | Familia visual | Uso |
| --- | --- | --- |
| Purple | Morado | Marca, interacción y acción |
| Info | Azul | Información semántica únicamente |
| Success | Verde | Resultado positivo |
| Warning | Ámbar | Advertencia o atención |
| Danger | Rojo | Error, riesgo o acción peligrosa |

**Primary NO representa estados. Info NO representa branding.**

---

## 8. Tipografía

La familia tipográfica oficial de la interfaz es **Inter**.

El código DEBE centralizar la escala tipográfica y evitar tamaños locales arbitrarios.

La escala debe contemplar como mínimo los siguientes roles:

```text
display
heading-1
heading-2
heading-3
body
small
caption
mono
```

### Reglas

- `body` es el nivel normal de lectura de interfaz.
- `small` se utiliza para información secundaria de densidad moderada.
- `caption` se reserva para información auxiliar y no debe transformarse en el tamaño habitual de contenido.
- `heading-*` expresa jerarquía real, no solo aumento visual.
- El producto DEBE mantener una jerarquía tipográfica consistente entre vistas.
- No se permiten familias tipográficas propias por feature.
- Datos técnicos, hashes o identificadores pueden utilizar la familia monoespaciada del sistema.
- Los valores exactos de tamaño, peso y `line-height` pertenecen a `tokens.css`.

---

## 9. Espaciado, forma y elevación

### 9.1 Espaciado

El sistema DEBE utilizar una única escala de espaciado centralizada.

Debe poder distinguir claramente:

- separación interna de controles;
- separación entre elementos relacionados;
- separación entre grupos;
- separación entre secciones.

Una feature NO DEBE crear una escala paralela.

### 9.2 Radios

Los radios DEBEN provenir de una escala común y responder a roles visuales consistentes.

No se permiten radios distintos por preferencia local cuando ya existe un rol equivalente.

### 9.3 Bordes y sombras

Los bordes son el mecanismo preferido para separar superficies ordinarias.

Las sombras DEBERÍAN reservarse para elevación real, como overlays, menús flotantes o elementos que se sitúan temporalmente sobre el contenido.

---

## 10. Movimiento

El movimiento debe comunicar transición, cambio de estado o relación espacial.

- Las duraciones DEBEN provenir de tokens.
- Las transiciones DEBEN ser breves y discretas.
- Se DEBE respetar `prefers-reduced-motion`.
- Ninguna información esencial puede depender de una animación.
- No se debe retrasar artificialmente una tarea solo para mostrar una animación decorativa.

---

## 11. Plataforma y layout

### 11.1 Alcance de dispositivo

PubTube UI soporta **desktop únicamente**.

El mínimo de referencia es **1280 × 720**, optimizando la experiencia para resoluciones habituales entre **1366 px y 1920 px de ancho**.

Esto no autoriza layouts rígidos: la interfaz DEBE soportar correctamente redimensionamiento dentro del rango de escritorio definido.

No se implementan variantes móviles ni patrones táctiles específicos mientras no exista un requisito de producto.

### 11.2 Navegación principal

La navegación principal utiliza un **navigation rail fijo y no colapsable**.

- Su ancho efectivo pertenece a `--layout-navigation-rail-width`.
- La barra superior utiliza `--layout-topbar-height` y el contenido de
  dashboard puede limitarse mediante `--layout-dashboard-width`.
- No se utiliza el antiguo token de sidebar para el layout aprobado.
- El contenido principal DEBE considerar permanentemente su presencia.
- El estado activo DEBE ser reconocible sin depender únicamente del color.
- La navegación NO DEBE cambiar de patrón entre vistas sin una razón funcional.

### 11.3 Estructura de página

Una vista puede contener, según contexto:

1. contexto de navegación;
2. título y descripción;
3. acciones principales;
4. filtros o controles de consulta;
5. contenido principal;
6. información secundaria;
7. feedback relacionado con la acción actual.

No todas las vistas necesitan todas estas regiones.

### 11.4 Overflow

- La página completa NO DEBE generar scroll horizontal accidental.
- Contenido inherentemente ancho puede tener overflow controlado dentro de su propia región.
- El overflow NO DEBE utilizarse para ocultar un layout mal resuelto.

---

## 12. Jerarquía de acciones e interacción

### 12.1 Acción primaria

Cada contexto DEBERÍA tener una única acción primaria dominante.

Puede existir más de una únicamente cuando representen acciones independientes con jerarquía equivalente y exista una justificación clara.

### 12.2 Acciones destructivas

Una acción destructiva DEBE distinguirse semánticamente.

La confirmación adicional se exige cuando la acción:

- es irreversible;
- provoca pérdida significativa de información;
- tiene consecuencias difíciles de recuperar;
- afecta recursos o procesos relevantes.

No toda acción de eliminación necesita automáticamente un modal si puede deshacerse o su impacto es trivial.

### 12.3 Acciones asíncronas

Cuando una acción está en ejecución:

- se DEBE evitar la ejecución duplicada cuando pueda generar efectos repetidos;
- el estado de progreso DEBE ser visible cerca del origen de la acción;
- las regiones no relacionadas NO DEBERÍAN bloquearse innecesariamente.

---

## 13. Formularios y validación

La estrategia de validación depende del contexto y del tipo de error.

Puede validarse:

- durante la escritura, cuando la corrección inmediata sea útil y no genere ruido;
- al abandonar un campo, cuando el dato pueda validarse de forma independiente;
- al enviar, cuando la validación dependa del conjunto completo o del backend.

### Reglas

- El placeholder NO reemplaza al label.
- Los errores DEBEN asociarse claramente al dato o acción que los originó.
- Un error DEBE explicar qué debe corregirse cuando esa información esté disponible.
- La validación NO DEBE castigar al usuario mostrando errores prematuramente sin utilidad.
- Los requisitos provenientes del backend DEBEN representarse sin inventar reglas de negocio en el frontend.

---

## 14. Estados de interfaz y feedback

Toda vista o acción asíncrona DEBE contemplar los estados que realmente pueda alcanzar.

### 14.1 Loading

- Para contenido estructural, DEBERÍAN utilizarse skeletons que mantengan aproximadamente la forma final.
- Los spinners DEBERÍAN reservarse para acciones locales, operaciones pequeñas o situaciones donde un skeleton no aporte contexto.
- No se debe bloquear contenido independiente.

### 14.2 Empty

Un estado vacío debe explicar, cuando corresponda:

1. qué falta;
2. por qué puede estar vacío;
3. qué acción permite continuar.

### 14.3 Error

El error debe aparecer preferentemente cerca del contexto que falló y debe indicar:

- qué no pudo completarse;
- qué parte se vio afectada;
- qué puede hacerse a continuación, si existe recuperación.

Los códigos técnicos pueden complementar el mensaje, pero no sustituirlo.

### 14.4 Success

El feedback positivo DEBE ser proporcional a la acción y mostrarse preferentemente en el mismo contexto donde ocurrió.

Ejemplos válidos:

- una acción cambia temporalmente a estado de éxito;
- una región actualizada refleja inmediatamente el resultado;
- un modal muestra brevemente el resultado antes de cerrarse cuando el flujo termina dentro de él.

No se establece un sistema global de toasts como requisito base. Un mecanismo global solo debe introducirse si una necesidad real no puede resolverse de forma contextual.

### 14.5 Feedback persistente

Un error que requiere intervención del usuario DEBE permanecer visible hasta que sea resuelto, reemplazado por un nuevo estado o descartado de forma consciente.

Los éxitos triviales PUEDE ser transitorios.

---

## 15. Overlays y cierre de contexto

Cuando se utilice un modal u overlay:

- `Escape` DEBE cerrarlo por defecto cuando no exista una razón para impedirlo;
- click fuera PUEDE cerrarlo en flujos normales;
- el foco DEBE gestionarse correctamente;
- al cerrar, el foco DEBE volver a un lugar coherente;
- el contenido detrás NO DEBE quedar operable de forma accidental;
- acciones destructivas o irreversibles DEBEN explicar claramente su consecuencia.

Si existen cambios sin guardar, el cierre accidental mediante `Escape`, click exterior u otro mecanismo DEBE bloquearse o requerir confirmación.

---

## 16. Tablas y listados de datos

PubTube es una aplicación de gestión; las tablas y listados son patrones centrales.

Cuando el contexto lo requiera, DEBEN poder contemplar:

- ordenamiento;
- paginación;
- filtros;
- acciones por fila;
- loading;
- empty;
- error.

La selección múltiple NO DEBE incorporarse por defecto. Solo se agrega cuando exista una operación real sobre múltiples elementos.

### Reglas

- Una tabla se utiliza únicamente cuando la información sea realmente tabular.
- Los encabezados DEBEN describir claramente el contenido.
- Ordenamiento y filtros DEBEN reflejar estado visible y predecible.
- Las acciones por fila NO DEBEN competir visualmente con el dato principal.
- La paginación DEBE conservar el contexto de filtros y ordenamiento cuando corresponda.
- Si los datos provienen del backend, la UI NO DEBE simular capacidades de filtrado, ordenamiento o paginación que el contrato no pueda garantizar.

---

## 17. Estados de dominio

Los nombres de estados pertenecen al dominio y a sus contratos, no al Design System.

Cuando el backend exponga estados:

1. se identifica su significado;
2. se mapea a una semántica visual existente;
3. se evita crear un color propio por cada nombre de estado;
4. se conserva texto explícito para evitar depender solo del color.

Si la semántica de un estado no está clara, NO DEBE inferirse únicamente desde su nombre técnico.

---

## 18. Accesibilidad

El estándar obligatorio es **WCAG 2.2 nivel AA** en los criterios aplicables a la interfaz.

### 18.1 Teclado y foco

- Todo control operable mediante mouse DEBE tener una alternativa de teclado cuando exista semántica equivalente.
- El foco DEBE ser visible.
- No se elimina el outline sin un reemplazo equivalente.
- El orden de tabulación DEBE seguir el flujo lógico.
- Se evita `tabindex` positivo.

### 18.2 Semántica HTML

Se DEBEN preferir elementos HTML nativos antes de recrear controles con elementos genéricos y ARIA.

ARIA complementa HTML; no lo sustituye.

### 18.3 Contraste

Los valores efectivos de color DEBEN verificarse contra WCAG 2.2 AA.

La comprobación se realiza sobre los tokens implementados, no sobre valores copiados en documentación.

### 18.4 Áreas de interacción

El sistema DEBE centralizar tamaños estándar de controles y áreas de interacción en tokens.

Deben existir al menos dos densidades funcionales:

- **estándar**, para controles generales;
- **compacta**, para contextos densos como tablas y toolbars.

La variante compacta NO DEBE reducir legibilidad, foco visible ni operabilidad por teclado.

### 18.5 Movimiento

Se DEBE respetar `prefers-reduced-motion` y ninguna tarea esencial puede depender de animación.

---

## 19. Iconografía

La familia iconográfica oficial es **Lucide** y la integración vigente de Vue
es `@lucide/vue`. La versión efectiva pertenece a `package.json`.

### Reglas

- Los componentes Vue que necesiten iconos DEBEN importarlos desde `@lucide/vue`.
- No mezclar familias de iconos sin una necesidad explícita.
- Los iconos DEBEN seguir la escala visual definida en tokens.
- Un icono ambiguo NO DEBE sustituir texto necesario.
- Los iconos decorativos DEBEN ocultarse de tecnologías de asistencia cuando corresponda.
- Una acción representada solo mediante icono DEBE tener nombre accesible.

---

## 20. Contenido y microcopy

### 20.1 Idioma y tono

La interfaz utiliza **español** y trato de **tú**.

El lenguaje debe ser:

- directo;
- breve;
- específico;
- orientado a la acción;
- consistente con la terminología del dominio;
- libre de jerga técnica cuando no sea necesaria para el usuario.

La redacción actual no debe impedir una futura internacionalización, pero i18n no forma parte del alcance base.

### 20.2 Capitalización

Se utiliza **sentence case** como regla general.

### 20.3 Acciones

Las acciones DEBEN usar verbos que indiquen el resultado esperado.

Preferir:

```text
Guardar cambios
Programar publicación
Reintentar publicación
Eliminar publicación
```

Evitar textos genéricos como:

```text
Aceptar
OK
Sí
Continuar
```

cuando pueda describirse con precisión lo que ocurrirá.

### 20.4 Puntuación

Botones, labels y títulos breves NO DEBERÍAN terminar en punto.

Mensajes, explicaciones, errores y estados vacíos pueden utilizar redacción completa cuando mejore comprensión.

### 20.5 Errores

Un mensaje de error debe responder, cuando exista información suficiente:

1. qué ocurrió;
2. qué se vio afectado;
3. qué puede hacer el usuario ahora.

---

## 21. Fechas, horas y zona horaria

La convención visual del frontend es:

- fecha: `DD/MM/YYYY`;
- hora: formato de 24 horas;
- fecha y hora combinadas: conservar ambos formatos de forma consistente.

### Zona horaria

Cuando el backend proporcione una zona horaria asociada a una programación, la UI DEBE respetarla y mostrarla cuando su omisión pueda producir ambigüedad.

El frontend NO DEBE convertir silenciosamente una programación a la zona local del navegador si el contrato define otra zona.

Si el backend no entrega información suficiente para determinar la zona horaria, la UI debe seguir el contrato vigente o declarar la ambigüedad; no debe inventar una zona por conveniencia visual.

---

## 22. Estrategia de estilos en Vue

Los estilos visuales globales se dividen en:

```text
src/styles/tokens.css   -> valores y escalas del sistema
src/styles/global.css   -> base global, tipografía y estilos verdaderamente globales
```

Para estilos propios de una vista o unidad de UI en Vue se prefiere:

```vue
<style scoped>
/* estilos locales */
</style>
```

### Reglas

- No se introduce CSS Modules, Tailwind u otra estrategia paralela sin una necesidad explícita y una decisión técnica correspondiente.
- Los estilos locales DEBEN consumir tokens globales cuando exista uno aplicable.
- Una feature NO DEBE redefinir globalmente tokens para alterar el sistema.
- Los overrides profundos sobre UI reutilizable NO DEBEN utilizarse para crear variantes ocultas.

---

## 23. Reutilización antes de creación

Los primitives reutilizables de la UI viven en [`src/shared/ui/`](../src/shared/ui/).
El código fuente es la fuente de verdad de sus props y emits; este documento
mantiene sus responsabilidades semánticas para evitar que una feature los
acople al dominio:

- `Button`, `IconButton` y `DateField` resuelven acciones y entrada de datos.
- `Avatar` resuelve identidad visual sin conocer usuarios del backend.
- `StatusBadge`, `StatusTab` y `KpiItem` expresan estados o métricas mediante
  semántica visual, sin decidir nombres de dominio.
- `NavigationRailItem` compone navegación accesible sin conocer rutas de negocio.

Estos componentes no realizan HTTP, no administran estado global y no contienen
lógica específica del Dashboard.

Antes de crear una nueva pieza de UI se DEBE:

1. buscar una solución existente en el repositorio;
2. comprobar si puede reutilizarse sin introducir comportamiento incorrecto;
3. preferir composición o extensión controlada antes que duplicación;
4. evitar crear una segunda solución para el mismo propósito;
5. mantener las necesidades específicas de dominio dentro de su feature cuando no sean realmente compartidas.

Una feature NO DEBE utilizar overrides profundos para convertir una solución compartida en una variante visual paralela.

Si aparece una necesidad estable y reutilizable, debe evolucionarse el sistema de forma explícita en vez de esconder la diferencia dentro de una feature.

---

## 24. Evolución y gobierno

No existe un propietario individual del Design System.

Cualquier cambio global DEBE seguir el proceso de revisión vigente del repositorio y aparecer explícitamente en el alcance de la tarea o PR correspondiente.

Un cambio semántico global NO DEBE introducirse incidentalmente mientras se implementa una feature.

### 24.1 Cambios que NO requieren modificar este documento

- cambiar un hexadecimal manteniendo su semántica;
- ajustar spacing, radius o tamaños manteniendo sus roles;
- cambiar una implementación interna;
- refactorizar estilos sin alterar reglas de uso;
- actualizar una dependencia sin cambiar el lenguaje visual.

### 24.2 Cambios que SÍ requieren revisarlo

- cambiar el significado de un token semántico;
- modificar la jerarquía de acciones;
- cambiar la plataforma soportada;
- introducir dark mode;
- cambiar la familia tipográfica oficial;
- cambiar la familia iconográfica oficial;
- alterar la política de navegación principal;
- cambiar reglas globales de accesibilidad, feedback o microcopy.

---

## 25. Checklist de diseño

Aplicar solo los puntos relevantes al cambio.

- [ ] Se reutilizó una solución existente cuando cumplía la misma responsabilidad.
- [ ] No se introdujeron valores visuales arbitrarios cuando existía un token aplicable.
- [ ] Los tokens utilizados representan intención, no apariencia accidental.
- [ ] No se creó una semántica o color paralelo para un concepto ya existente.
- [ ] La jerarquía entre acciones es clara.
- [ ] Las acciones destructivas tienen protección proporcional a su impacto.
- [ ] Los estados alcanzables de loading, empty, error y success están resueltos.
- [ ] El feedback aparece en el contexto adecuado.
- [ ] Los skeletons mantienen razonablemente la estructura del contenido final cuando se utilizan.
- [ ] Tablas y listados conservan filtros, ordenamiento y paginación de forma coherente cuando corresponda.
- [ ] La selección múltiple solo existe si hay una operación real que la necesite.
- [ ] La vista funciona desde 1280×720 dentro del alcance desktop.
- [ ] No existe scroll horizontal accidental a nivel de página.
- [ ] El navigation rail fijo mantiene una navegación consistente.
- [ ] El foco es visible y la interacción relevante funciona mediante teclado.
- [ ] La información no depende exclusivamente del color.
- [ ] Los colores efectivos cumplen WCAG 2.2 AA.
- [ ] Los iconos pertenecen a Lucide salvo excepción explícita.
- [ ] El contenido utiliza español, trato de tú y sentence case.
- [ ] Fechas y horas siguen la convención global.
- [ ] La zona horaria respeta la información entregada por el backend.
- [ ] No se agregó complejidad para mobile, dark mode o necesidades hipotéticas fuera de alcance.

---

## 26. Anti-patrones

Evitar:

- duplicar valores de tokens dentro de documentación;
- hardcodear colores, tipografía, spacing, radios o sombras repetibles;
- crear tokens distintos para el mismo significado;
- crear una paleta por feature;
- utilizar el color primario para todos los estados;
- diseñar para mobile cuando no forma parte del alcance;
- implementar dark mode preventivamente;
- hacer colapsable el navigation rail sin un requisito explícito;
- introducir selección múltiple sin una operación de lote real;
- utilizar modales o feedback global para confirmaciones triviales;
- mostrar errores lejos del contexto que los produjo cuando pueden mostrarse localmente;
- usar spinners de página completa cuando solo una región está cargando;
- reducir controles compactos hasta comprometer legibilidad o accesibilidad;
- crear nuevas piezas de UI sin revisar primero el repositorio;
- crear variantes ocultas mediante overrides profundos;
- inferir comportamiento de estados o zonas horarias que el backend no haya definido;
- documentar como regla un detalle que el código ya expresa de forma inequívoca y cuya variación no cambia la semántica.

---

## 27. Regla de decisión rápida

Ante una nueva necesidad visual:

```text
¿Ya existe una solución con el mismo propósito?
├─ Sí -> reutilizarla.
└─ No
   ↓
¿La necesidad es específica de una feature?
├─ Sí -> resolverla localmente sin crear una regla global.
└─ No
   ↓
¿Existe una semántica global equivalente?
├─ Sí -> reutilizarla o crear un alias semántico si mejora claridad.
└─ No
   ↓
¿La necesidad es estable y reutilizable?
├─ No -> mantenerla local hasta tener evidencia.
└─ Sí -> extender explícitamente el sistema y centralizar su implementación.
```

El objetivo del Design System no es acumular reglas o abstracciones, sino **reducir inconsistencias con el menor número de conceptos necesarios**.
