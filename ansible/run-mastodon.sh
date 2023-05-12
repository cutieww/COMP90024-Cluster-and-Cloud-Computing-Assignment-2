#!/usr/bin/env bash

. ./secrets.sh; ansible-playbook -u ubuntu -i /home/wagw/COMP90024-Cluster-and-Cloud-Computing-Assignment-2/ansible/inventory/inventory.ini mastodon.yaml --check

# use -K for sudo password 

