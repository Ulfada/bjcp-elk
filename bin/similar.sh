#!/usr/bin/env bash
SERVER=${SERVER:-"http://elastic.docker.localhost"}
BEER=${BEER:-"7B"}
SIZE=${SIZE:-10}
set -e

echo "### Searchgin for beer: $BEER"
VECTOR=$(curl -s -X GET "$SERVER/bjcp/_doc/$BEER?pretty" -H 'Content-Type: application/json' | jq --compact-output "._source.vector")
echo "### Found vector: $VECTOR"
curl -f -s -X POST "$SERVER/bjcp/_search?pretty" -H 'Content-Type: application/json' -d $'{
  "query": {
    "script_score": {
      "query": {
        "exists": {
          "field": "vector"
        }
      },
      "script": {
        "source": "1 / (1 + l2norm(params.query_vector, doc[\u0027vector\u0027]))",
        "params": {
          "query_vector":'${VECTOR}'
        }
      }
    }
  },
  "size": '${SIZE}',
  "_source": {
    "includes": [
      "_id",
      "vector",
      "vital_avg",
      "subcategory"
    ]
  }
}' | jq  --compact-output  ".hits.hits[] | { "score": ._score, "id": ._id, "name": ._source.subcategory, "vector": ._source.vector, "vital": ._source.vital_avg }"
