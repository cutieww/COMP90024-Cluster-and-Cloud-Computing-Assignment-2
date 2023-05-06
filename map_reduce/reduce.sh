# bin/bash
npm install
echo "npm install finish"

export dbname1="mastodon_policy"
export user="admin"
export pass="admin"
grunt couch-compile
grunt couch-push
echo "map reduce compile finish"

# policy_count Mastodon_policy
curl -XGET "http://admin:admin@172.26.128.252:5984/mastodon_policy/_design/mastodon_policy/_view/policy_count?reduce=true" > "result/mastodon/policy_count.json"

curl -XGET "http://admin:admin@172.26.128.252:5984/mastodon_policy/_design/mastodon_policy/_view/user_count?group=true" > "result/mastodon/user_count.json"



# curl -XGET "http://admin:admin@172.26.128.252:5984/mastodon_policy/_design/mastodon/_view/user_count?group=true&descending=true" > "result/user_count.json"


# curl -XGET "http://admin:admin@172.26.128.252:5984/twitter/_design/policy_count/_view/gcc_count?group=true" > "result/gcc_count.json"
