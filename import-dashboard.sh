#!/usr/bin/env bash
KIBANA_URL=${KIBANA_URL:-http://kibana.docker.localhost}
FILE=${FILE:-./dashboard.json}

set -e

echo "### Importing BJCP Kibana dashboard"
curl -f --silent --output /dev/null  -X POST "$KIBANA_URL/api/kibana/dashboards/import" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' --data-binary @./dashboard.json

echo "### Success, visit: ${KIBANA_URL}"
