#!/bin/sh
# Merge modular OpenTelemetry Collector YAML files into a single config file.
# Usage: ./scripts/merge-otel-config.sh
# This script is used by the Makefile target 'otel'.
# It generates observability/config/otel_collector/config/otel-collector-config.yaml from modular YAML files.


DIR="observability/config/otel_collector/config"
OUT="observability/config/otel_collector/config/otel-collector-config.generated.yaml"

{
    echo
    cat "$DIR/receivers.yaml"

    echo
    cat "$DIR/processors.yaml"

    echo
    cat "$DIR/exporters.yaml"

    echo
    cat "$DIR/pipelines.yaml"

} > "$OUT"

echo "Merged config written to $OUT"
