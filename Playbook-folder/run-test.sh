#!/usr/bin/env bash

. ./secrets.sh
export URL='https://mastodon.au/api/v1'

# Test access 
curl --header "Authorization: Bearer ${MASTODON_ACCESS_TOKEN=}" \
     -XGET \
     -vvv \
  	 "${URL}/accounts/verify_credentials" | jq
