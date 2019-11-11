#!/usr/bin/env bash
KIBANA_URL=${KIBANA_URL:-http://kibana.docker.localhost}
DASHBOARD_ID=${DASHBOARD_ID:-0d040ef0-0068-11ea-932d-092d2997e124}
FILE=${FILE:-./dashboard.json}

set -e

echo "### Exporting bjcp dashboard to $FILE"
curl -f -X GET "$KIBANA_URL/api/kibana/dashboards/export?dashboard=$DASHBOARD_ID" -H 'kbn-xsrf: true' -o $FILE

