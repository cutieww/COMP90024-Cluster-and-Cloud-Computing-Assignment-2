import couchdb
import requests
import json
import time

#host_ip = "192.168.1.116" # Note: if running locally, use the host machine IP
#host_ip = "172.26.132.19"
host_ip = "172.26.129.100" # replalce this with instance IP the server Running

couch = couchdb.Server(f'http://admin:admin@{host_ip}:5984')
db = couch['mastodon_policy']


def mastodon_user_count():
    map_function = """
    function (doc) {
    if (doc.political_related== true){
        emit(doc.username,1)
    }
    }
    """

    view_name = "user_count"
    design_doc_name = "_design/policy_view"

    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,  
            "views": {
                view_name: {
                    "map": map_function,
                    "reduce": "_count"
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

    print("try to get the total mastodon count for political related topics")
    url = f'http://admin:admin@{host_ip}:5984/mastodon_policy/_design/policy_view/_view/user_count?group=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true"
    response = requests.get(url)
    data = json.loads(response.text)
    user_dict = dict()
    for row in data['rows']:
        user_dict[row["key"]] = row["value"]
    sorted_user_dict = dict(sorted(user_dict.items(), key=lambda item: item[1], reverse=True))

    return sorted_user_dict




def mastodon_total_count():
    map_function = """
    function (doc) {
    if (doc.political_related== true){
        emit(doc._id,1)
    }
    }
    """

    view_name = "policy_count"
    design_doc_name = "_design/policy_view"

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

    print("try to get the total mastodon count for political related topics")
    url = f'http://admin:admin@{host_ip}:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true"
    response = requests.get(url)
    data = json.loads(response.text)
    count = data['rows'][0]['value']
    return count



mastodon_data = {'number': 0, 'host': host_ip}
if __name__ == '__main__':
    time.sleep(1)
    while True:
        
        total_count  = mastodon_total_count()
        print("Number of policy related topic in mastodon:", total_count)
        mastodon_data['number'] = total_count
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_data)

        mastodon_user = mastodon_user_count()
        print("Number of post for each unique user:", mastodon_user)
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_user)





        time.sleep(1)
