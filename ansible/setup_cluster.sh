
curl -XPOST "http://admin:admin@172.26.132.54:5984/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"admin\", \"password\":\"admin\", \"port\": \"5984\",\
             \"remote_node\": \"172.26.135.122\", \"node_count\": \"$(echo 172.26.135.122 | wc -w)\",\
             \"remote_current_user\":\"admin\", \"remote_current_password\":\"admin\"}"

curl -XPOST "http://admin:admin@172.26.132.54:5984/_cluster_setup"\
      --header "Content-Type: application/json"\
      --data "{\"action\": \"add_node\", \"host\":\"172.26.135.122\",\
             \"port\": \"5984\", \"username\": \"admin\", \"password\":\"admin\"}"

curl -XPOST "http://admin:admin@172.26.132.54:5984/_cluster_setup"\
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"

curl -X GET "http://admin:admin@172.26.135.122:5984/_membership"

