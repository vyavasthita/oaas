# Observability as a Service (OAAS)

- Standalone observability stack that any backend can reuse over a shared Docker network.
- Services push OTLP telemetry via [Instrumentation Hub](https://github.com/vyavasthita/instrumentation-hub)
- OAAS handles storage, routing, and visualization.

**Example consumer:** [Auth Service](https://github.com/vyavasthita/auth-service)

---

## Architecture

```mermaid
flowchart LR
    subgraph Your Service
        App((FastAPI App)) -->|instrumentation-hub| OTLP[OTLP Exporters]
    end
    OTLP -->|logs/traces/metrics| Collector[OTel Collector]
    Collector --> Loki
    Collector --> Tempo
    Collector --> Prometheus
    Prometheus --> Alertmanager --> Discord
    Loki --> Grafana
    Tempo --> Grafana
    Prometheus --> Grafana
```

---

## Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| OTel Collector | 0.95.0 | OTLP ingest + routing |
| Loki | 2.9.4 | Log storage |
| OpenSearch | 2.11.0 | Full-text log search |
| Tempo | 2.5.0 | Trace storage |
| Jaeger | 1.57 | Alternate trace UI |
| Prometheus | 2.49.1 | Metrics + alerting rules |
| Alertmanager | 0.27.0 | Alert routing (Discord) |
| Grafana | 10.4.2 | Unified dashboards |

---

## Getting Started

### Option A — Dev Container (Recommended)

**Prerequisites:** VS Code, Docker Desktop, [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

1. Clone this repo
2. Configure [`.env`](.env) (see table below)
3. Open the folder in VS Code
4. When prompted, click **Reopen in Container** (or run `Dev Containers: Reopen in Container` from the command palette)
5. All 9 observability services start automatically
6. Access Grafana at `http://localhost:1001`

> No Python, Make, or other tooling needed on the host — everything runs inside containers.

### Option B — Makefile

**Prerequisites:** Docker Desktop / Docker Engine + Compose, Make

1. Clone this repo
2. Configure [`.env`](.env) (see table below)
3. Run:
   ```bash
   make up       # creates network, merges OTel config, boots stack
   make ps       # check health
   ```

### `.env` Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OBSERVABILITY_NETWORK_NAME` | `oaas-observability-net` | Shared Docker network |
| `GRAFANA_ADMIN_USER` | `admin` | Grafana username |
| `GRAFANA_ADMIN_PASSWORD` | `admin` | Grafana password |
| `GRAFANA_HOST_PORT` | `1001` | Grafana |
| `PROMETHEUS_HOST_PORT` | `1002` | Prometheus |
| `ALERTMANAGER_HOST_PORT` | `1003` | Alertmanager |
| `LOKI_HOST_PORT` | `1004` | Loki |
| `TEMPO_HOST_PORT` | `1005` | Tempo |
| `JAEGER_HOST_PORT` | `1006` | Jaeger |
| `OPENSEARCH_CORE_HOST_PORT` | `1007` | OpenSearch (direct) |
| `OPENSEARCH_PROXY_HOST_PORT` | `1008` | OpenSearch proxy |
| `OTEL_COLLECTOR_GRPC_HOST_PORT` | `1009` | Collector gRPC |
| `OTEL_COLLECTOR_HTTP_HOST_PORT` | `1010` | Collector HTTP |
| `OTEL_COLLECTOR_PROMETHEUS_HOST_PORT` | `1011` | Collector Prometheus exporter |

For alerting: `export DISCORD_WEBHOOK_URL=<URL>`

### Make Commands

```bash
make up       # creates network, merges OTel config, boots stack
make ps       # check health
make logs     # follow logs
make stop     # stop (preserve volumes)
make down     # stop + remove
make clean    # stop + remove + prune volumes
```

---

## Service Endpoints

| Service | URL | Variable |
|---------|-----|----------|
| Grafana | http://localhost:1001 | `GRAFANA_HOST_PORT` |
| Prometheus | http://localhost:1002 | `PROMETHEUS_HOST_PORT` |
| Alertmanager | http://localhost:1003 | `ALERTMANAGER_HOST_PORT` |
| Loki | http://localhost:1004 | `LOKI_HOST_PORT` |
| Tempo | http://localhost:1005 | `TEMPO_HOST_PORT` |
| Jaeger | http://localhost:1006 | `JAEGER_HOST_PORT` |
| OpenSearch | http://localhost:1008 | `OPENSEARCH_PROXY_HOST_PORT` |
| OTel Collector (HTTP) | http://localhost:1010 | `OTEL_COLLECTOR_HTTP_HOST_PORT` |

---

## Integrating Another Repository

1. **Join the shared network** — add to your `docker-compose.yaml`:
   ```yaml
   networks:
     observability:
       external: true
       name: ${OBSERVABILITY_NETWORK_NAME}
   ```
   `OBSERVABILITY_NETWORK_NAME` in your `.env` must match the value in OAAS `.env`.

2. **Set env vars** in your service container:
   ```yaml
   OTEL_EXPORTER_LOGS_ENDPOINT: http://otel-collector:4318/v1/logs
   OTEL_EXPORTER_TRACES_ENDPOINT: http://otel-collector:4318/v1/traces
   OTEL_EXPORTER_METRICS_ENDPOINT: http://otel-collector:4318/v1/metrics
   OTEL_SERVICE_NAME: <your-service>
   LOGGING_BACKEND: loki          # or opensearch
   TRACING_BACKEND: tempo         # or jaeger
   METRICS_BACKEND: prometheus
   ```

3. **Install [Instrumentation Hub](https://github.com/vyavasthita/instrumentation-hub)**:
   ```bash
   poetry add git+https://github.com/vyavasthita/instrumentation-hub.git#subdirectory=packages/python/fastapi
   ```

4. **Wire it up** in your FastAPI app:
   ```python
   from instrumentation_hub_fastapi import FastAPIInstrumentation
   FastAPIInstrumentation().setup(app)
   ```



5. **Verify** — hit your service, then check Grafana Explore.

> See [Auth Service](https://github.com/vyavasthita/auth-service) for a complete working example.

---

## Documentation

- [Implementation guide](observability/docs/main.md) · [Common concepts](observability/docs/common.md)
- [Logs](observability/docs/logs.md) · [Metrics](observability/docs/metrics.md) · [Traces](observability/docs/traces.md)
- [Grafana provisioning](observability/docs/grafana.md) · [Alerting](observability/docs/alerting.md)

---

## Related Repositories

| Repository | Purpose |
|------------|---------|
| [Instrumentation Hub](https://github.com/vyavasthita/instrumentation-hub) | Client library for instrumenting FastAPI services |
| [Auth Service](https://github.com/vyavasthita/auth-service) | Example consumer — JWT auth service with full OAAS integration |

---

## Troubleshooting

```bash
make ps                              # check container health
curl http://localhost:1004/ready     # Loki readiness
curl http://localhost:1005/ready     # Tempo readiness
make logs                            # stream all logs
```

---

## License

Copyright © 2026 Dilip Kumar Sharma. All rights reserved.
