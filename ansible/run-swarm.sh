#!/usr/bin/env bash


ansible-playbook -u ubuntu -i /home/wagw/COMP90024-Cluster-and-Cloud-Computing-Assignment-2/ansible/inventory/inventory.ini docker_swarm.yaml

# use -K for sudo password 

