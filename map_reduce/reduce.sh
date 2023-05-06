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
curl -XGET "http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true" > "result/mastodon/policy_count.json"

curl -XGET "http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/user_count?group=true" > "result/mastodon/user_count.json"

