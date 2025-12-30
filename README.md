# Tic Tac Toe Backend & Observability

A modular FastAPI backend for Tic Tac Toe (N players and bot) with full observability using Docker Compose and future Kubernetes support.

---

## About the Project
- Play Tic Tac Toe with multiple players and a bot
- Built with Python and FastAPI
- Includes MySQL 8, MySQL Workbench, PhpMyAdmin
- Observability: OpenTelemetry Collector, Loki, Prometheus, Grafana

---

## Software & Libraries
- Python 3.13.1
- Docker, Docker Compose
- GNU Make
- MySQL, PhpMyAdmin, MySQL Workbench
- OpenTelemetry, Loki, Prometheus, Grafana

---

## System Environment
- Docker Compose v2.31.0-desktop.2
- Docker v27.4.0
- GNU Make 3.81
- Python 3.13.1

---


## Directory Structure
```
observability/
  config/         # Static config files
    otel_collector/
      config/
        receivers.yaml     # Modular OTel Collector config: receivers
        processors.yaml    # Modular OTel Collector config: processors
        exporters.yaml     # Modular OTel Collector config: exporters
        pipelines.yaml     # Modular OTel Collector config: service/pipelines
        otel-collector-config.generated.yaml # Auto-generated merged config (do not edit directly)
  data/           # Runtime data (Loki, Prometheus, Grafana)
backend/          # FastAPI backend
scripts/          # Project scripts (e.g., merge-otel-config.sh)
```

---

## Installation & Run
```bash
# Clone repo
$ git clone https://github.com/vyavasthita/tic-tac-toe.git
$ cd tic-tac-toe
$ git checkout master

# Start all services
$ make all
```

---

## Access Services
- **FastAPI Docs:** http://localhost:5000/docs
- **PhpMyAdmin:** http://localhost:8081/
- **MySQL Workbench:** http://localhost:3000/
- **Prometheus:** http://localhost:9090/
- **Grafana:** http://localhost:8080/ (user: admin, pass: admin)

---

## Observability
- OpenTelemetry Collector: Collects logs from backend, exports to Loki
- Loki: Stores and indexes logs
- Prometheus: Scrapes metrics (can be extended)
- Grafana: Visualizes logs and metrics
- Config files: `observability/config/`, data: `observability/data/`

**How log capture works:**
- The OpenTelemetry LoggingHandler is attached to the root logger in our backend. This means every log message—no matter which part of the app or library it comes from—is intercepted, enriched with resource attributes (like service name), and exported as an OpenTelemetry log record.
- The LoggingHandler ensures all logs are consistently formatted and sent to the OpenTelemetry Collector endpoint, where they are processed and forwarded to Loki for storage and Grafana for visualization.

---

## Stopping & Cleaning
```bash
# Stop all containers
$ make stop
# Remove all containers and data
$ make clean
```

---

## Kubernetes (Planned)
- Helm charts and manifests will be added for full K8s deployment
- Modular config ready for Kubernetes in `observability/config/`
- To run with Minikube:
  ```bash
  minikube start --memory=4098
  make helm
  ```

---

## References
- [Observability Zero to Hero](https://github.com/iam-veeramalla/observability-zero-to-hero/)
- [OpenTelemetry & Python Guide](https://www.cncf.io/blog/2022/04/22/opentelemetry-and-python-a-complete-instrumentation-guide/)
- [FastAPI Monitoring with Grafana & Prometheus](https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn)

---

## Roadmap
- [ ] Add Kubernetes manifests and Helm charts
- [ ] Extend observability to metrics and traces
- [ ] Add more dashboards and alerting

---

## Contributing
See [Contributors](https://github.com/vyavasthita/grhakarya/graphs/contributors)

---

## Code of Conduct
TBD

---

For details on observability flow, see [`observability/docs/observability-working.md`](observability/docs/observability-working.md).