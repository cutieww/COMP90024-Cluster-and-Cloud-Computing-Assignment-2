#!/usr/bin/env bash

# ansible-galaxy collection install openstack.cloud:2.0.0

. ./secrets.sh; ansible-playbook -u ubuntu docker_swarm.yaml

# use -K for sudo password 

