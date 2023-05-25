#!/bin/bash

# Team 84 - Melbourne
# Brendan Pichler(bpichler@student.unimelb.edu.au) 1212335
# George Wang (wagw@student.unimelb.edu.au) 1084224
# Luchen Zhou(luczhou@student.unimelb.edu.au) 1053412
# Wei Wang(wangw16@student.unimelb.edu.au) 900889
# Yihan Wang (yihwang3@student.unimelb.edu.au) 1056614

# Configuration
NODE_TO_REMOVE="couchdb@172.26.128.32"
COUCHDB_USERNAME="admin"
COUCHDB_PASSWORD="admin"

# Remove the node from the _nodes database
REV=$(curl -s -X GET "http://${COUCHDB_USERNAME}:${COUCHDB_PASSWORD}@172.26.128.32:5984/_node/_local/_nodes/${NODE_TO_REMOVE}" | jq -r '._rev')
curl -X DELETE "http://${COUCHDB_USERNAME}:${COUCHDB_PASSWORD}@172.26.128.32:5984/_node/_local/_nodes/${NODE_TO_REMOVE}?rev=${REV}"

# List all databases
DBS=$(curl -s -X GET "http://${COUCHDB_USERNAME}:${COUCHDB_PASSWORD}@172.26.128.32:5984/_all_dbs" | jq -r '.[]')

# Iterate over each database
for DB in $DBS; do
  # Get the shard map
  SHARD_MAP=$(curl -s -X GET "http://${COUCHDB_USERNAME}:${COUCHDB_PASSWORD}@172.26.128.32:5986/_dbs/${DB}")

  # Remove the node from the shard map
  UPDATED_SHARD_MAP=$(echo "$SHARD_MAP" | jq "del(.by_node.\"${NODE_TO_REMOVE}\") | del(.by_range[] | select(.[] | contains(\"${NODE_TO_REMOVE}\"))[0])")

  # Update the shard map
  curl -X PUT "http://${COUCHDB_USERNAME}:${COUCHDB_PASSWORD}@172.26.128.32:5986/_dbs/${DB}" -H "Content-Type: application/json" -d "${UPDATED_SHARD_MAP}"
done

# Check the membership
curl -X GET "http://${COUCHDB_USERNAME}:${COUCHDB_PASSWORD}@172.26.128.32:5984/_membership"

