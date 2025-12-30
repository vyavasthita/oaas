
# How Observability Works in This Project

---


This document explains the end-to-end flow of logging observability in our FastAPI backend, including the roles of OpenTelemetry Collector, Loki, Prometheus, and Grafana, and how configuration files drive the process.

---


**OTLP Endpoints:**

- `OTEL_EXPORTER_LOGS_ENDPOINT = http://otel-collector:4318/v1/logs`
- `OTEL_EXPORTER_TRACES_ENDPOINT = http://otel-collector:4318/v1/traces`
- `OTEL_EXPORTER_METRICS_ENDPOINT = http://otel-collector:4318/v1/metrics`

---

## Protocols Used in the Log Pipeline: OTLP vs REST

# This file has been split for clarity and maintainability.

- For common OpenTelemetry and observability concepts, see: [observability-common.md](observability-common.md)
- For logging-specific observability details, see: [observability-logs.md](observability-logs.md)
- For metrics-specific observability details, see: [observability-metrics.md](observability-metrics.md)
- For traces-specific observability details, see: [observability-traces.md](observability-traces.md)



# Consolidated Observability Block Diagram



```mermaid
flowchart LR
APP[FastAPI App]
COLLECTOR[OpenTelemetry Collector]
LOKI[Loki (Logs)]
TEMPO[Tempo (Traces)]
PROM[Prometheus (Metrics)]
GRAFANA[Grafana]
APP --|Logs (OTLP)| COLLECTOR
APP --|Traces (OTLP)| COLLECTOR
APP --|Metrics (OTLP)| COLLECTOR
COLLECTOR --|Logs| LOKI
COLLECTOR --|Traces| TEMPO
COLLECTOR --|Metrics| PROM
LOKI --|Logs| GRAFANA
TEMPO --|Traces| GRAFANA
PROM --|Metrics| GRAFANA

APP[FastAPI App]

COLLECTOR[OpenTelemetry Collector]

LOKI[Loki (Logs)]

TEMPO[Tempo (Traces)]

PROM[Prometheus (Metrics)]

GRAFANA[Grafana]

APP --|Logs (OTLP)| COLLECTOR
APP --|Traces (OTLP)| COLLECTOR
APP --|Metrics (OTLP)| COLLECTOR

COLLECTOR --|Logs| LOKI
COLLECTOR --|Traces| TEMPO
COLLECTOR --|Metrics| PROM

LOKI --|Logs| GRAFANA
TEMPO --|Traces| GRAFANA
PROM --|Metrics| GRAFANA

APP[FastAPI App]
COLLECTOR[OpenTelemetry Collector]
LOKI[Loki (Logs)]
TEMPO[Tempo (Traces)]
PROM[Prometheus (Metrics)]
GRAFANA[Grafana]

APP --|Logs (OTLP)| COLLECTOR
APP --|Traces (OTLP)| COLLECTOR
APP --|Metrics (OTLP)| COLLECTOR

COLLECTOR --|Logs| LOKI
COLLECTOR --|Traces| TEMPO
COLLECTOR --|Metrics| PROM

LOKI --|Logs| GRAFANA
TEMPO --|Traces| GRAFANA
PROM --|Metrics| GRAFANA
```

---

## Key Points

- All configuration is modular and separated for maintainability.
- Data directories are kept separate from config for clean operation.
- The flow is extensible: we can add metrics/traces by updating Collector config and backend setup.
- Grafana provides a single pane of glass for all observability data.

---

For more details, see the implementation checklist and config files in the `observability/config/` directory.
