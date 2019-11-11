#!/usr/bin/env bash
KIBANA_URL=${KIBANA_URL:-http://kibana.docker.localhost}
FILE=${FILE:-./dashboard.json}

set -e
set -x

echo "### Importing the dashboard"
curl -f -X POST "$KIBANA_URL/api/kibana/dashboards/import" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' --data-binary @./dashboard.json

set +x
echo
echo "### Now Go to kibana:"
echo "http://kibana.docker.localhost/"
