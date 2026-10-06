# Grafana: dashboard técnico del Gateway (US-D7-T4)

Grafana sirve para diagnóstico técnico de tráfico, errores y latencia. Vue 3
es la UI funcional del producto; no es esta interfaz ni un iframe de Grafana.
Este repositorio agrega únicamente Grafana y consume Prometheus existente.

```text
PubTube-Mod4
  ├── Gateway :8000       /api/health y /metrics
  └── Prometheus :9090    job="pubtube-gateway"
          │
          │ pubtube-network (Docker)
          ▼
PubTube-ui
  └── Grafana :3000       datasource -> http://prometheus:9090
```

Los puertos mostrados son valores por defecto. Los puertos host de Gateway y
Prometheus pueden configurarse en backend; el puerto interno de Prometheus
permanece 9090. `localhost:9090` se usa desde el host, nunca como datasource
dentro de Grafana. La red externa `pubtube-network` la crea el compose backend.

## Archivos y fuente de verdad

- `docker-compose.observability.yml`: solo Grafana OSS **13.2.3**, puerto host
  local configurable y almacenamiento de datos. Sin plugins descargados
  automáticamente; se usan los paneles y datasource incluidos en la imagen.
- `observability/grafana/provisioning/datasources/prometheus.yml`: datasource
  `pubtube-prometheus`, proxy, default y solo lectura.
- `observability/grafana/provisioning/dashboards/dashboards.yml`: proveedor
  de archivos en carpeta `PubTube`, sin actualizaciones desde la UI.
- `observability/grafana/dashboards/pubtube-gateway.json`: dashboard
  `pubtube-gateway`, título `PubTube Gateway`, `editable: false`.
- `tasks/us-d7-t4-grafana.jsonl`: contrato ordenado y dependencias.
- `scripts/observability/verify_grafana.py`: comprobación API reproducible con
  biblioteca estándar Python; evita depender de clicks como evidencia.

Provisioning y dashboard se montan read-only. Editar en Git, revisar y recrear
Grafana cuando cambie datasource/provider; el proveedor recarga dashboard cada
10 segundos. El volumen conserva usuarios/preferencias; no es la fuente del
datasource ni del dashboard. Credenciales iniciales solo se aplican al crear
una base de datos nueva; cambiar la variable no resetea un usuario existente.

## Arranque integrado

1. Tener Docker/Compose disponible. En un checkout de **PubTube-Mod4/develop**,
   sin editar sus archivos, ejecutar:

```sh
docker compose up --build -d --wait
```

El backend actual también inicia sus servicios de trazas existentes. Esta
tarea no los añade ni modifica. Revisar `.env`/variables locales del backend
para determinar puertos reales y evitar conflictos con stacks ya activos.

2. Desde el host, verificar Gateway y Prometheus (ejemplo con puertos default):

```sh
curl --fail http://localhost:8000/api/health
curl --fail http://localhost:9090/-/healthy
curl --fail http://localhost:9090/api/v1/targets
docker network inspect pubtube-network
```

En targets, `labels.job` debe ser `pubtube-gateway` y `health` debe ser `up`.
No crear otro Prometheus ni una red alternativa para ocultar un fallo.

3. En la raíz de **PubTube-ui**, definir `GRAFANA_ADMIN_USER` (default `admin`)
y `GRAFANA_ADMIN_PASSWORD` en el entorno. La contraseña es obligatoria, no tiene
un default versionado. Ejemplo PowerShell sin guardar el secreto en historial:

```powershell
$env:GRAFANA_ADMIN_USER = 'admin'
$grafanaCredential = Get-Credential -UserName $env:GRAFANA_ADMIN_USER -Message 'Credenciales locales de Grafana'
$env:GRAFANA_ADMIN_PASSWORD = $grafanaCredential.GetNetworkCredential().Password
docker compose -f docker-compose.observability.yml config --quiet
docker compose -f docker-compose.observability.yml up -d --wait
```

En POSIX, capturar la contraseña sin eco y exportarla:

```bash
export GRAFANA_ADMIN_USER=admin
read -r -s -p 'Grafana password: ' GRAFANA_ADMIN_PASSWORD
export GRAFANA_ADMIN_PASSWORD
docker compose -f docker-compose.observability.yml config --quiet
docker compose -f docker-compose.observability.yml up -d --wait
```

`GRAFANA_PORT` permite cambiar 3000 si está ocupado. Se publica solo en loopback
del host. Puede usarse un archivo local ignorado con `--env-file <ruta-local>`;
no versionar sus valores ni imprimir `docker compose config` expandido con
credenciales reales. `config --quiet` valida sin mostrarlas.

4. Abrir [Grafana local](http://localhost:3000) (o el puerto configurado),
iniciar sesión con las credenciales y navegar a **Dashboards -> PubTube ->
PubTube Gateway**, o ir directamente a `/d/pubtube-gateway`.

5. Generar tráfico seguro al Gateway. Por ejemplo PowerShell:

```powershell
1..10 | ForEach-Object { Invoke-RestMethod 'http://localhost:8000/api/health' | Out-Null; Start-Sleep -Seconds 1 }
```

Esperar al menos dos scrapes (intervalo backend 15 s); `rate` y p95 necesitan
muestras. No provocar fallos destructivos para obtener 5xx.

6. Verificar paneles y APIs con el comprobador, manteniendo credenciales en entorno:

```sh
python scripts/observability/verify_grafana.py
```

Por defecto consulta Gateway `http://localhost:8000`, Prometheus
`http://localhost:9090` y Grafana `http://localhost:3000`. Si los puertos host
cambian, definir `GATEWAY_URL`, `PROMETHEUS_URL` y `GRAFANA_URL` con sus URLs
reales; esto no cambia el DNS del datasource dentro del contenedor.
Puede usarse `.venv` existente o cualquier Python 3.10+; no requiere paquetes.

El check devuelve exit code 0 únicamente si comprueba healths, target UP,
datasource read-only/health OK, dashboard provisionado idéntico en paneles y
queries, series counter/histogram, y datos finitos en las siete consultas
operativas tanto por Prometheus como por el proxy del datasource Grafana.
Usa `/api/datasources/uid/pubtube-prometheus`, su `/health`,
`/api/dashboards/uid/pubtube-gateway` y
`/api/datasources/proxy/uid/pubtube-prometheus/api/v1/query`.
Los endpoints legacy están disponibles en la versión fijada; verificar su
compatibilidad al actualizar Grafana. Envía pocas requests de health y espera
scrapes mediante reintentos acotados; no instala ni modifica servicios.

## Paneles y métricas

| Panel | Datos y unidad |
| --- | --- |
| Gateway status | `up{job="pubtube-gateway"}`: UP/DOWN; No data si falta target. |
| Requests por minuto | `sum(rate(pubtube_gateway_requests_total{job="pubtube-gateway"}[1m])) * 60`, req/min. |
| Requests por status class | Rate por `status_class`, req/s; solo clases observadas. |
| Errores 5xx | Rate con `status_class="5xx"`, req/s; cero si no hay serie y target UP. |
| p95 latency | Histogram buckets, segundos; umbral visible **0.3 s (300 ms)**. |
| p95 por ruta | Histogram por `le, route`, segundos; línea de umbral 0.3 s. |
| Requests por ruta | Rate por `route` normalizada, req/s. |

Todas las queries operativas filtran `job="pubtube-gateway"`. Solo utilizan
`pubtube_gateway_requests_total` (method, route, status_class),
`pubtube_gateway_request_duration_seconds_bucket` (method, route, le)
y `up`. Las unidades son segundos o requests/minuto/segundo según el cálculo.
El refresh es 15 s, rango inicial 30 minutos y ventanas rate de 1m/5m.
El panel 5xx no convierte un target DOWN en cero saludable.
La medición p95 es diagnóstica: no demuestra el objetivo bajo carga.

La row colapsada **Future — RabbitMQ / Publications** contiene el aviso:

> These panels may show No data until the corresponding backend/exporter exposes these metrics.

Sus queries preparadas usan únicamente `rabbitmq_queue_messages_ready`,
`rabbitmq_queue_messages_unacked`, `pubtube_publications_scheduled_total`,
`pubtube_publications_completed_total` y `pubtube_publications_failed_total`.
No presuponen labels ni disponibilidad actual, no añaden exporters y se excluyen
de la evidencia runtime. No usar como actuales las métricas de upstream,
rate limiting o auth failures que solo estén planificadas.

## Prueba de reconstrucción (AC5)

En un entorno de validación con almacenamiento Grafana desechable:

```sh
python scripts/observability/verify_grafana.py
docker compose -f docker-compose.observability.yml down --volumes
docker compose -f docker-compose.observability.yml up -d --wait
python scripts/observability/verify_grafana.py
```

`down --volumes` elimina el volumen **de este compose Grafana**, incluyendo
usuarios/preferencias. Usarlo solo para la prueba indicada; para detener sin
eliminar datos, omitir `--volumes`. La red externa y el backend permanecen.
Mantener las mismas variables de entorno para recrear credenciales iniciales.
El segundo check demuestra que datasource y dashboard reaparecen con una base
vacía, usando únicamente archivos versionados, sin configuración manual previa.

## Validación estática y diagnóstico

```sh
python -m compileall -q agents
python -m pytest -q agents/tests
python -m json.tool observability/grafana/dashboards/pubtube-gateway.json
docker compose -f docker-compose.observability.yml config --quiet
git diff --check
```

El contrato tiene siete registros JSON por línea, IDs únicos, order 0..6 y
dependencias del registro anterior. Comprobar `json.loads()` por línea,
campos obligatorios, IDs únicos y dependencias anteriores antes de ejecutarlo.
JSON/YAML válidos y Compose config **no prueban** connectivity, queries ni
reprovisioning. Si Docker/backend no están disponibles, registrar NOT VERIFIED
para AC runtime y reportar PARTIAL/BLOCKED, sin declarar DONE.

- Red externa inexistente: levantar primero backend y comprobar network inspect.
- Datasource health falla: comprobar DNS `prometheus`, red y puerto interno 9090;
  desde Grafana, `wget -q -O - http://prometheus:9090/-/healthy`.
- Dashboard ausente: revisar mounts y logs de provisioning Grafana.
- No data: revisar target, generar health requests y esperar scrapes; la row
  Future puede permanecer sin datos indefinidamente hasta instrumentación futura.
- Login falla tras cambiar variable: el usuario existente vive en el volumen;
  cambiar contraseña por el mecanismo Grafana, sin borrar datos necesarios.

Referencias oficiales: [provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/),
[Grafana OSS 13.2.3](https://grafana.com/grafana/download/13.2.3?edition=oss),
[API datasource](https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/api-legacy/data_source/).
