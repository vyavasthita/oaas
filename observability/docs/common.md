# OpenTelemetry & Observability: Common Concepts

---

This document covers the foundational concepts, protocols, and architecture patterns used for observability in this project, including OpenTelemetry, Collector, and backend integration. It is intended as a shared reference for all telemetry types (logs, metrics, traces).

---

## Shared Instrumentation Toolkit

Every FastAPI service now reuses [instrumentation-hub](https://github.com/vyavasthita/instrumentation-hub) (specifically the `instrumentation-hub-fastapi` package) instead of duplicating OTLP wiring. The helper ships:

- Cached Pydantic settings for `OTEL_*` environment variables.
- Logging/tracing/metrics exporters preconfigured for OAAS.
- Request metrics middleware plus the Prometheus exposition app.

This keeps all services aligned with the same semantic conventions and drastically reduces the surface area of per-repo observability code. Future adapters (Django, Express, etc.) will follow the same pattern so this document applies across languages.

> Context: the repository now exposes observability as a standalone service. Client applications connect over a shared Docker network and push OTLP telemetry into the stack.

---

## Signal Routing via Resource Attributes

Instrumentation Hub automatically stamps three resource attributes on every log/span/metric:

| Attribute | Supported Values | Purpose |
|-----------|------------------|---------|
| `logging_backend` | `loki`, `opensearch` | Tells the Collector whether to ship logs to Loki or the elasticsearch-compatible stack.
| `tracing_backend` | `tempo`, `jaeger` | Fans traces to Tempo (default) or the new Jaeger backend.
| `metrics_backend` | `prometheus` | Reserves future expansion for alternate metrics sinks.

Set the matching `*_BACKEND` environment variables (e.g., `TRACING_BACKEND=jaeger`) in each workload to pick a
single destination per signal without editing OAAS config. A service therefore emits logs to exactly one logging
backend, traces to exactly one tracing backend, and so on. Because the collector keeps every exporter active
(Tempo+Jaeger, Loki+OpenSearch), multiple services can stream telemetry simultaneously even if they choose
different combinations.

---

## Protocols Used in the Observability Pipeline

### OTLP vs REST

- **OTLP (OpenTelemetry Protocol):**
  - Purpose-built for telemetry (logs, metrics, traces).
  - Defines a strict, efficient, and standardized data model (Protobuf/JSON).
  - Supports HTTP and gRPC transports.
  - Enables batching, compression, and streaming.
  - Ensures interoperability and future-proofing across OpenTelemetry-compatible tools.

- **REST API:**
  - Generic, vendor-agnostic, but not optimized for telemetry.
  - Used by some backends (e.g., Loki) for log ingestion.

### Push vs Pull: Data Movement

| Step                                   | Mechanism | Who initiates?               |
|----------------------------------------|-----------|------------------------------|
| App → OTEL Collector                   | Push      | App (OTLP exporter)          |
| OTEL Collector → Backend (e.g., Loki)  | Push      | Collector (Exporter)         |
| Backend Storage                        | Passive   | Backend only receives        |

- **Push:** Sender initiates and transmits data.
- **Pull:** Receiver fetches data (not used in this pipeline).
- **Passive:** Backend listens for incoming data.

**Summary:**
- All steps from app to backend are push-based. No pull mechanism is used.

---

## Why OTLP Instead of a Generic REST API?

- **Purpose-built for Telemetry:**
  - Strict, efficient, and standardized data model for logs, metrics, and traces.
  - Ensures compatibility and semantic consistency.
- **Optimized for Observability:**
  - Supports batching, compression, streaming, and high-throughput.
- **Interoperability and Future-proofing:**
  - Seamless integration between SDKs, Collectors, and backends.
  - Evolves with the observability ecosystem.

**Summary:**
- OTLP is a full protocol and data model for observability, not just a transport.
- REST is generic but lacks telemetry-specific features.
- OpenTelemetry uses OTLP for all agent/collector communication.

---

## OpenTelemetry Collector: Central Pipeline

- Receives, processes, and exports telemetry data (logs, metrics, traces).
- Modular config allows future extension for all telemetry types.
- Acts as a bridge between OTLP and backend-specific protocols (e.g., REST for Loki).

---

## Configuration Structure

- Modular config files for receivers, processors, exporters, and pipelines.
- Merged into a single config for the Collector service.
- Data directories are kept separate from config for clean operation.

---

## Extensibility

- The architecture is designed to support logs, metrics, and traces by updating Collector config and backend setup.
- Each telemetry type will have its own detailed documentation file, referencing this common document for shared concepts.

---

For details on logs, see [logs.md](logs.md).
For metrics, see [metrics.md](metrics.md).
For traces, see [traces.md](traces.md).
