#!/usr/bin/env bash

. ./secrets.sh; ansible-playbook -u ubuntu -i ~/inventory/inventory.ini mastodon.yaml

