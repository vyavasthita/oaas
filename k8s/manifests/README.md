# Kubernetes Manifests for Tic-Tac-Toe

This directory contains Kubernetes manifests for deploying the full observability stack, backend, and database for the Tic-Tac-Toe project.

## Structure
- Each service (database, backend, observability, etc.) has its own manifest YAML file.
- ConfigMaps and Secrets are used for configuration and sensitive data.
- Node Exporter and kube-state-metrics are included for infrastructure monitoring.
- Ingress is used for external access to services.

## Usage
- Use `kubectl apply -f .` in this directory to deploy all resources.
- See the Makefile in the project root for cluster management commands.

---

**Note:** All ports and endpoints are configured via ConfigMaps for flexibility. Update these as needed for your environment.
