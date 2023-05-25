#!/bin/bash

# Team 84 - Melbourne
# Brendan Pichler(bpichler@student.unimelb.edu.au) 1212335
# George Wang (wagw@student.unimelb.edu.au) 1084224
# Luchen Zhou(luczhou@student.unimelb.edu.au) 1053412
# Wei Wang(wangw16@student.unimelb.edu.au) 900889
# Yihan Wang (yihwang3@student.unimelb.edu.au) 1056614

# Set the IP addresses of the master and worker nodes
master_ip="172.26.132.19"
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

