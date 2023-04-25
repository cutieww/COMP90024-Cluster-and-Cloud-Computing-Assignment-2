import couchdb
import requests
import json
import time

couch = couchdb.Server('http://admin:admin@localhost:5984')
db = couch['db_test']

map_function = """
function (doc) {
  emit(null, 1);
}
"""

view_name = "count_docs"
design_doc_name = "_design/document_count"

if design_doc_name not in db:
    design_doc = {
        "_id": design_doc_name,
        "views": {
            view_name: {
                "map": map_function,
                "reduce": "_sum"
            }
        }
    }
    db.save(design_doc)
else:
    design_doc = db[design_doc_name]
    if view_name not in design_doc["views"]:
        design_doc["views"][view_name] = {
            "map": map_function,
            "reduce": "_sum"
        }
        db.save(design_doc)

def count_documents():
    url = f"http://admin:admin@localhost:5984/db_test/_design/document_count/_view/count_docs?reduce=true&group_level=0"
    response = requests.get(url)
    data = json.loads(response.text)
    document_count = data['rows'][0]['value']
    return document_count

mastodon_data = {'number': 0}
if __name__ == '__main__':
    time.sleep(1)
    while True:
        total_count  = count_documents()
        print("Number of documents:", total_count)
        mastodon_data['number'] = total_count
        requests.post('http://localhost:8000/update_mastodon', json=mastodon_data)
        time.sleep(1)
