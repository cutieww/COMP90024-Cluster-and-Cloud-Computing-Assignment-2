#!/bin/bash

# Set the IP addresses of the master and worker nodes
master_ip="172.26.129.100"
worker_ip="172.26.128.252"

# Use the IP addresses in the curl commands
curl -XPOST "http://admin:admin@$master_ip:5984/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"admin\", \"password\":\"admin\", \"port\": \"5984\",\
             \"remote_node\": \"$worker_ip\", \"node_count\": \"$(echo $worker_ip | wc -w)\",\
             \"remote_current_user\":\"admin\", \"remote_current_password\":\"admin\"}"

curl -XPOST "http://admin:admin@$master_ip:5984/_cluster_setup"\
      --header "Content-Type: application/json"\
      --data "{\"action\": \"add_node\", \"host\":\"$worker_ip\",\
             \"port\": \"5984\", \"username\": \"admin\", \"password\":\"admin\"}"

curl -XPOST "http://admin:admin@$master_ip:5984/_cluster_setup"\
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"

curl -X GET "http://admin:admin@$worker_ip:5984/_membership"

