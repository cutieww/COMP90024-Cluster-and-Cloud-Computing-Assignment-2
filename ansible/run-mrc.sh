#!/usr/bin/env bash

ansible-galaxy collection install openstack.cloud:2.0.0

. ./openrc.sh; ansible-playbook -u ubuntu -i inventory/inventory.ini  mrc.yaml --check