
# How Observability Works in This Project

---


This document explains the end-to-end flow of logging observability in our FastAPI backend, including the roles of OpenTelemetry Collector, Loki, Prometheus, and Grafana, and how configuration files drive the process.

---

**OTLP Endpoint:**

`OTEL_COLLECTOR_OTLP_ENDPOINT = http://otel-collector:4318`

---

## Protocols Used in the Log Pipeline: OTLP vs REST


# This file has been split for clarity and maintainability.

- For common OpenTelemetry and observability concepts, see: `observability-common.md`
- For logging-specific observability details, see: `observability-logs.md`

# (In the future, add similar files for metrics and traces.)
    D[Grafana]
    E[Prometheus]

    A -- OTLP logs --> B
    B -- Loki push --> C
    C -- Grafana query --> D
    A -- Metrics --> E
    E -- Grafana query --> D
```

---

## 5. Key Points

- All configuration is modular and separated for maintainability.
- Data directories are kept separate from config for clean operation.
- The flow is extensible: we can add metrics/traces by updating Collector config and backend setup.
- Grafana provides a single pane of glass for all observability data.

---

For more details, see the implementation checklist and config files in the `observability/config/` directory.
