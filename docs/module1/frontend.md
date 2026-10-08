# Frontend e integración del Módulo 1

Este documento registra qué pantallas de PubTube Studio se conectan al backend
NestJS inspeccionado en el workspace (`pubtube-modulo1`) y qué funciones siguen
siendo solo visuales. El frontend permanece en este repositorio Vue; no se
modifica el backend desde esta tarea.

## Pantallas implementadas

1. **Biblioteca:** filtros de período y estado, resumen, tabla y paginación. Usa
   fixtures visibles como demostración porque no existe una ruta de catálogo.
2. **Editar metadatos:** admite un `contentId` real, carga versión actual e
   historial, permite consultar una versión puntual y guardar una nueva versión.
   Los elementos de la biblioteca demo nunca generan llamadas ni aparentan
   guardar datos reales.
3. **Carga pausada por duplicado:** acepta MP4/MOV, calcula SHA-256 en bloques,
   inicializa multipart, consulta partes, sube directamente a Garage por URLs
   prefirmadas y ensambla. Un `409 DUPLICATE_CONTENT` lleva al estado pausado con
   `existingContentId`.

## Contratos HTTP confirmados

| Operación | Ruta | Uso en la UI |
| --- | --- | --- |
| Crear multipart | `POST /api/content/init` | Envía filename, MIME, sizeBytes y SHA-256; maneja 409 de duplicado. |
| Obtener URL para una parte | `GET /api/content/:sessionId/part/:partNumber` | La respuesta contiene `{ url }`; el navegador envía la parte con `PUT` a Garage. |
| Consultar partes | `GET /api/content/upload/:sessionId/status` | Carga las partes completadas de la sesión. |
| Completar multipart | `POST /api/content/upload/:sessionId/complete` | Envía `{ parts: [{ PartNumber, ETag }] }`; recibe contentId y checksum verificado. |
| Leer versión actual e historial | `GET /api/content/:contentId` | Devuelve `metadata` e `historial`. |
| Leer metadatos actuales | `GET /api/content/:contentId/metadata` | Disponible en backend; la UI usa la ruta combinada anterior para evitar una segunda consulta. |
| Leer versión puntual | `GET /api/content/:contentId/metadata/versions/:version` | Permite consultar versiones anteriores. |
| Crear versión de metadatos | `PUT /api/content/:contentId/metadata` | Envía title, description, tags y visibility (`public`, `unlisted`, `private`). |

El cliente agrega `x-correlation-id` a las llamadas NestJS. No lo agrega a las
peticiones de bytes a Garage ni envía el archivo al servidor NestJS.

## Funciones no conectadas

- **Catálogo paginado, agregados/contadores y búsqueda:** no existe endpoint
  HTTP; las filas y cifras de biblioteca son fixtures etiquetados como demo.
- **Programación:** la transición está parcialmente en servicios internos, pero
  no hay endpoint HTTP para programar. La fecha no se envía y la acción está
  deshabilitada.
- **Nombre, tamaño y preview para un `contentId` existente:** las rutas de
  metadatos no exponen estos datos ni una URL reproducible. Para contenido real
  solo se muestra su ID; el control de preview está deshabilitado.
- **Cancelar/eliminar sesión multipart:** no hay ruta HTTP. “Detener envío” solo
  aborta la solicitud del navegador; la sesión remota queda bajo la política de
  limpieza/lifecycle del backend. No se afirma que el servidor la canceló.
- **Cuenta/canal YouTube:** no se crea ni se inventa una identidad de canal.

## Gateway y CI del Módulo 1

La integración del módulo con el Gateway usa esta configuración:

| Parámetro | Valor M1 |
| --- | --- |
| `MODULE_SLOT` | `1` |
| `MODULE_PORT` | `8000` |
| Health interno | `GET /health` |
| Smoke test público | `GET /api/content/health` |
| Host interno en la red Docker | `http://module1-api:8000` |
| Gateway público informado | `http://148.116.105.83:8000` |
| Imagen GHCR prevista | `ghcr.io/sebasinmas/pubtube-modulo1:develop` |

El Gateway enruta `/api/content/health` a `/health` y las rutas `/api/content`
de contenido hacia M1. La tabla de endpoints de producto arriba describe las
rutas públicas de contenido. La GitHub Action del módulo debe ejecutar pruebas,
construir la imagen, iniciar módulo y Gateway y pasar el smoke test a través del
Gateway antes de publicar. Solo publica en un `push` a `develop` y requiere
`contents: read` y `packages: write`. Tras el primer push se debe habilitar la
descarga pública del paquete desde GitHub Packages.

## Requisitos para integración runtime

1. Configurar `VITE_API_BASE_URL` con la URL del Gateway (el endpoint público
   informado es `http://148.116.105.83:8000`). La variable solo contiene una URL
   pública, nunca credenciales.
2. El Gateway smoke-test usa `Authorization: Bearer <JWT>`. El cliente HTTP del
   frontend aún no adjunta ese encabezado; antes de probar endpoints protegidos
   se necesita acordar cómo obtiene la UI un JWT válido. No guardar JWTs ni
   secretos en variables `VITE_*`.
3. El backend M1 llama `SessionValidator` en `POST /init` y `PUT metadata`.
   Esta UI no implementa login; el entorno debe proporcionar la sesión válida.
4. El origen del frontend debe estar permitido por el Gateway y Garage debe
   permitir CORS desde el navegador para `PUT` y exponer `ETag`; sin eso no se
   puede completar multipart. Esa configuración aún no se verificó.
5. En CI, el contenedor debe responder en el puerto `8000` con `GET /health`.
   El smoke test del Gateway usa la ruta `/api/content/health` y un JWT temporal
   de CI; no reutilizar el secreto de prueba en producción.

Por estas dependencias, build y pruebas unitarias no demuestran conectividad
runtime con NestJS ni Garage.
