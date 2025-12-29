# Observability Implementation Steps


This document summarizes the essential steps to enable observability (logging, metrics, tracing) in a Python/FastAPI project. Use this as a checklist to replicate observability in other repositories.

---

## Directory Structure for Observability

To keep configuration and runtime data cleanly separated and future-proof, this project uses the following structure:

```
observability/
	config/
		observability_backends/
			loki/
				config/
					loki-config.yaml
			prometheus/
				config/
					prometheus.yaml
		otel_collector/
			config/
				receivers.yaml
				processors.yaml
				exporters.yaml
				pipelines.yaml
				otel-collector-config.yaml
		grafana/
			provisioning/
				datasources/
					loki.yaml
				dashboards/
					...
	# (In the future, you could add:)
	# kubernetes/
	#   config/
	#     ...
data/
	loki/
		wal/
		chunks/
		index/
	prometheus/
		...
	grafana/
		...
```

- All static configuration for observability tools is under `observability/config/`.
- All runtime/mount/generated data is under `data/`.
- If you add Kubernetes or other platforms, you can add new directories under `observability/` (e.g., `observability/kubernetes/`).
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

---

## 6. OpenTelemetry Collector: Modular Log Pipeline

- The OpenTelemetry Collector is added as a Docker service for log collection and export to Loki.
- Config is split into modular files under `observability/config/otel_collector/config/`:
  - `receivers.yaml`: How logs are received (OTLP)
  - `processors.yaml`: Processing steps (batch)
  - `exporters.yaml`: Where logs are sent (Loki)
  - `pipelines.yaml`: Ties receivers, processors, and exporters
  - `otel-collector-config.yaml`: Main config (merged from above, see file for merge instructions)
- The Collector service is defined in `docker-compose.yaml` with line comments for clarity.
- This setup is log-only for now; metrics and traces can be added later by extending the modular config files.

---

