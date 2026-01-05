# Observability: Grafana Integration & Dashboard Management

This document describes how Grafana is configured, provisioned, and used inside the Observability-as-a-Service stack.

---

## Overview

Grafana is used to visualize metrics, logs, and traces from Prometheus, Loki, OpenSearch, and Tempo. Dashboards provide actionable insights into application health, performance, and business KPIs.

---

## Key Concepts
- **Data Sources:** Prometheus (metrics), Loki & OpenSearch (logs), Tempo (traces)
- **Dashboards:** Visual collections of panels for observability
- **Panels:** Visualizations (graphs, tables, stats, etc.)
- **Provisioning:** Automated setup of data sources and dashboards via config files and JSON

---

## Folder Structure
```
config/grafana/
    dashboards/                # Dashboard JSON files
    provisioning/
        datasources/           # Data source configs (YAML)
        dashboards/            # Dashboard provisioning configs (YAML)
docs/grafana.md
```

---

## Dashboard Provisioning
- Place exported dashboard JSON files in the `dashboards/` directory.
- Use provisioning YAML in `provisioning/dashboards/` to auto-load dashboards on container startup.
- Example: `dashboard.yaml` points to `/var/lib/grafana/dashboards` inside the container.

---

## Data Source Provisioning
- Use YAML files in `provisioning/datasources/` to define Prometheus, Loki, OpenSearch, and Tempo data sources.
- Files:
    - `prometheus.yaml` → Prometheus at `http://prometheus:9090`
    - `loki.yaml` → Loki at `http://loki:3100`
    - `opensearch.yaml` → OpenSearch Logs at `http://opensearch:9200` (pre-configured for the `otel-logs-*` index)
    - `tempo.yaml` → Tempo at `http://tempo:3200`

---

## Importing & Exporting Dashboards
- **Export:** In Grafana UI, open a dashboard → Settings → JSON Model → Export.
- **Import:** In Grafana UI, click "+" → Import → Upload JSON or paste JSON.
- **Provision:** Place JSON in the dashboards folder and restart Grafana (if using provisioning).

---

## Best Practices
- Use clear, descriptive panel titles and legends.
- Group related panels into logical dashboards (e.g., Application Overview, HTTP Metrics, Database Health).
- Use variables for flexible dashboards (e.g., filter by service, endpoint, status code).
- Version control dashboard JSON and provisioning configs.
- Document dashboard purpose and key queries in markdown panels.

---

## User Management & Security
- Default admin user/password is set via environment variables in docker-compose.
- For production, change default credentials and consider enabling authentication (OAuth, LDAP, etc.).
- Set up user roles and permissions as needed.

---

## Troubleshooting
- If dashboards do not appear, check provisioning logs in Grafana container.
- Ensure dashboard JSON and YAML files are valid and correctly mounted.
- Verify data source connectivity (Prometheus, Loki, Tempo).

---

## References
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Provisioning Dashboards](https://grafana.com/docs/grafana/latest/administration/provisioning/#dashboards)
- [Provisioning Data Sources](https://grafana.com/docs/grafana/latest/administration/provisioning/#data-sources)
