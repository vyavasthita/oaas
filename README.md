# Tic Tac Toe Backend & Observability

A modular FastAPI backend for Tic Tac Toe (N players and bot) with full observability using Docker Compose and future Kubernetes support.

---

## About the Project
- Play Tic Tac Toe with multiple players and a bot
- Built with Python and FastAPI
- Includes MySQL 8, MySQL Workbench, PhpMyAdmin
- Observability: OpenTelemetry Collector, Loki, Prometheus, Grafana

---

## System Environment

| Tool/Service              | Version/Info                |
|--------------------------|-----------------------------|
| Python                   | 3.13.1                      |
| Docker                   | 27.4.0                      |
| Docker Compose           | v2.31.0-desktop.2           |
| GNU Make                 | 3.81                        |
| MySQL                    | 8.0.29                      |
| PhpMyAdmin               | 5.2.1                       |
| MySQL Workbench          | 8.0.28                      |
| OpenTelemetry Collector  | 0.95.0                      |
| Loki                     | 2.9.4                       |
| Tempo                    | 2.5.0                       |
| Prometheus               | v2.49.1                     |
| Alertmanager             | v0.27.0                     |
| Grafana                  | 10.4.2                      |

---

### Prerequisite: Set Discord Webhook for Alertmanager

Before starting the stack, export your Discord webhook URL as an environment variable so Alertmanager can send alerts to Discord:

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
```

This ensures the Alertmanager container receives the webhook URL securely from your host environment.

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

### Access Services

| Service           | URL                                 | Notes                      |
|-------------------|-------------------------------------|----------------------------|
| FastAPI Docs      | http://localhost:5000/docs          |                            |
| PhpMyAdmin        | http://localhost:8081/              |                            |
| MySQL Workbench   | http://localhost:3000/              |                            |
| Loki              | http://localhost:3100/              |                            |
| Tempo             | http://localhost:3200/              |                            |
| Prometheus        | http://localhost:9090/              |                            |
| Alertmanager      | http://localhost:9093/              |                            |
| Grafana           | http://localhost:8080/              | user: admin, pass: admin   |

---

### Observability
- OpenTelemetry Collector: Collects logs from backend, exports to Loki ([Overview](observability/docs/observability.md))
- Loki: Stores and indexes logs ([Logging](observability/docs/observability-logs.md))
- Prometheus: Scrapes metrics (can be extended) ([Metrics](observability/docs/observability-metrics.md))
- Tempo: Stores and indexes traces ([Traces](observability/docs/observability-traces.md))
- Alertmanager: Routes alerts to notification channels (email, Slack, etc.) ([Alerting](observability/docs/observability-alerting.md))
- Grafana: Visualizes logs, metrics, traces, and alerts

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