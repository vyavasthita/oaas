# Observability Implementation Steps

This document summarizes the essential steps to enable observability (logging, metrics, tracing) in a Python/FastAPI project. Use this as a checklist to replicate observability in other repositories.

---



## 1. Docker Compose: Observability Services

### 1.1 Grafana
- Add Grafana for visualization (metrics and logs).
- Mount configuration files for Grafana provisioning.
- Expose required ports (e.g., 3000 for UI).

### 1.2 Loki
- Add Loki for log aggregation and storage (see Loki Integration section for details).
- Expose required port (3100).

### 1.3 General
- For each service, only add environment variables and volumes needed for logging/Loki (avoid unrelated config here).



## 2. Backend Logging

### 2.1 Logging Module
- Implement a centralized logging module in your backend (e.g., `observability/logging.py`).

### 2.2 Log Format
- Ensure all logs are structured in JSON format and output to stdout (so Loki can ingest them).

### 2.3 Initialization
- Configure logging at app startup, before initializing FastAPI.

### 2.4 Dependencies
- Only core dependencies (FastAPI, Uvicorn, etc.) and logging-related packages are required at this stage.





## 3. Loki & Promtail Integration

### 3.1 Loki Service Setup
- Use the `grafana/loki` image in your docker-compose.yaml.
- Expose port `3100` for Loki's HTTP API.

### 3.2 Loki Configuration
- Mount a config file from `./data/loki/loki-config.yaml` to `/etc/loki/local-config.yaml` in the container.
- Place all Loki config and data under `./data/loki` for clarity.
- Example config for local/dev is provided in `loki-config.yaml` (see `data/loki/loki-config.yaml`).

### 3.3 Networking
- Connect Loki to the same Docker network as backend and Grafana (e.g., `tic-tac-toe-network`).

### 3.4 Grafana Integration
- Add a Grafana data source config for Loki in `grafana/provisioning/datasources/loki.yaml` so Grafana can connect to Loki automatically.





## 4. Prometheus & Grafana (To be added later)

### 4.1 Prometheus
- Prometheus and metrics-related configuration will be added in a later step.

### 4.2 Grafana Metrics
- Grafana metrics dashboards and integration will be added in a later step.



## 5. OpenTelemetry (To be added later)

### 5.1 Tracing & Metrics
- OpenTelemetry and tracing/metrics configuration will be added in a later step.

---

## References
- [Grafana Loki Docs](https://grafana.com/docs/loki/latest/)
- [Prometheus Docs](https://prometheus.io/docs/introduction/overview/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [FastAPI Logging](https://fastapi.tiangolo.com/advanced/custom-loggers/)
