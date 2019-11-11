#!/usr/bin/env bash
SERVER_URL=${SERVER_URL:-http://elastic.docker.localhost}
FILE=${FILE:-./bjcp-es.json}

echo "### Drop Elasticsearch index: bjcp"
curl --silent --output /dev/null -XDELETE "$SERVER_URL/bjcp"

set -e

echo "### Create index with settings"
curl -f -XPUT -H "Content-Type: application/json" "$SERVER_URL/bjcp?pretty" --data-binary  @./settings.json

echo "### Update mapping"
curl -f -XPUT -H "Content-Type: application/json" "$SERVER_URL/bjcp/_mapping" --data-binary  @./mappings.json

echo
echo "### Import BJCP Style Guide"
curl -f --silent --output /dev/null -XPOST -H "Content-Type: application/json" "$SERVER_URL/bjcp/_bulk" --data-binary  @${FILE}

echo "### Elasticsearch index bjcp provisionned successfully"

