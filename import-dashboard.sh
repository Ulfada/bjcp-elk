#!/usr/bin/env bash
SERVER_URL=${SERVER_URL:-http://elastic.docker.localhost}
KIBANA_URL=${KIBANA_URL:-http://kibana.docker.localhost}
FILE=${FILE:-./bjcp-es.json}

set -e
set -x

echo "### Drop index"
curl -XDELETE "$SERVER_URL/bjcp"

echo "### Create index with settings"
curl -f -XPUT -H "Content-Type: application/json" "$SERVER_URL/bjcp?pretty" --data-binary  @./settings.json

echo "### Set a mapping"
curl -f -XPUT -H "Content-Type: application/json" "$SERVER_URL/bjcp/_mapping" --data-binary  @./mappings.json

echo "### Bulk import"
curl -f -XPOST -H "Content-Type: application/json" "$SERVER_URL/bjcp/_bulk" --data-binary  @${FILE}

echo "### Importing the dashboard"
curl -f -X POST "$KIBANA_URL/api/kibana/dashboards/import" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' --data-binary @./dashboard.json

set +x
echo
echo "### Now Go to kibana:"
echo "http://kibana.docker.localhost/"
