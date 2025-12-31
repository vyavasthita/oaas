#!/bin/sh
# Replace placeholder with environment variable
if [ -z "$DISCORD_WEBHOOK_URL" ]; then
  echo "DISCORD_WEBHOOK_URL is not set"
  exit 1
fi

sed "s|__DISCORD_WEBHOOK_URL__|$DISCORD_WEBHOOK_URL|g" /etc/alertmanager/alertmanager.yaml.template > /etc/alertmanager/alertmanager.yaml

# Start Alertmanager with the generated config
exec /bin/alertmanager --config.file=/etc/alertmanager/alertmanager.yaml
