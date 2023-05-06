import couchdb
import json

host_ip = "172.26.128.252"
couch = couchdb.Server(f'http://admin:admin@172.26.128.252:5984')


# cluster_nodes = ['http://node1.example.com:5984', 'http://node2.example.com:5984']
# cluster = couchdb.Cluster(cluster_nodes)

# session = cluster.session()

db = couch['mastodon_policy']


mastodon_policy = {
    "_id": "_design/mastodon",
    "views": {
        "policy_count": {
            "map": "function (doc) {\n  if (doc.political_related == true) {\n    emit(doc._id, 1);\n  }\n}",
            "reduce": "_sum"
        }
    }
}

mastodon_count = {
    "_id": "_design/mastodon",
    "views": {
        "favouraite_count": {
            "map": "function (doc) {\n  if (doc.political_related == true) {\n    emit(doc.username, favourites_count);\n  }\n}",
            "reduce": "_count"
        }
    }
}



result = db.view('mastodon/favouraite_count', reduce=True)


db.save(mastodon_count)

count = result.rows[0].value


with open('policy_count.json', 'w') as f:
    json.dump(count, f)

print(f"Count: {count}")





