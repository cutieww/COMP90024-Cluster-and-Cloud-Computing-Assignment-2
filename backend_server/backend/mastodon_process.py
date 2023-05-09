import couchdb
import requests
import json
import time
import datetime

#host_ip = "192.168.1.116" # Note: if running locally, use the host machine IP
#host_ip = "172.26.132.19"
host_ip = "172.26.129.100" # replalce this with instance IP the server Running

import datetime

# Get today's date
today = datetime.date.today()

# Format the date as a string in the desired format
date_string = today.strftime("%Y-%m-%d")

# Combine the date string with the CouchDB name prefix
db_name = "mastodon_policy_" + date_string


couch = couchdb.Server(f'http://admin:admin@{host_ip}:5984')
# db = couch['mastodon_policy']
db = couch[db_name]

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

def mastodon_count():
    map_function = """
    function (doc) {
        emit(null,1)
    }
    """

    view_name = "total"
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

    url = f'http://admin:admin@{host_ip}:5984/mastodon_policy/_design/policy_view/_view/total?reduce=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true"
    response = requests.get(url)
    data = json.loads(response.text)
    count = data['rows'][0]['value']
    return count

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
                "reduce": "_count"
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

def mastodon_user_total():
    map_function = """
    function (doc) {
        emit(doc.username,1)
    }
    """

    view_name = "user_total"
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
    url = f'http://admin:admin@{host_ip}:5984/mastodon_policy/_design/policy_view/_view/user_total?reduce=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true"
    response = requests.get(url)
    data = json.loads(response.text)
    count = data['rows'][0]['value']

    return count


def mastodon_word_map():
    map_function = """
    function(doc) {
    if (doc.political_related== true){
    var words = doc.token.split('|');
    for (var i = 0; i < words.length; i++) {
        if (!/^\d+$/.test(words[i])){
        emit(words[i], 1);
        }
        }
    }
    }
    """



    view_name = "word_count"
    design_doc_name = "_design/policy_view"

    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,  
            "views": {
                view_name: {
                    "map": map_function,
                    "reduce": "_count",
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function,
                "reduce": "_count",
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/mastodon_policy/_design/policy_view/_view/word_count?group=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?group=true"
    response = requests.get(url)
    data = json.loads(response.text)
    word_dict = dict()
    for row in data["rows"]:
        if row["key"] not in word_dict:
            word_dict[row["key"]] = row["value"]
    word_sort_dict = dict(sorted(word_dict.items(), key=lambda item: item[1], reverse=True))
    return word_sort_dict



mastodon_data = {'number': 0, 'host': host_ip}
mastodon_percentage = dict()
if __name__ == '__main__':
    time.sleep(1)
    while True:
        
        # number of post with related to the political related topics
        total_count  = mastodon_total_count()
        print("Number of policy related topic post in mastodon:", total_count)
        mastodon_data['number'] = total_count
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_data)

        
        # number of users that post include the political related topics
        mastodon_user = mastodon_user_count()
        print("Number of post for each unique user -- post")
        print("Number of post for each unique user:", mastodon_user)
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_user)


        # the percentage that include the post the political related topics and the username
        total  = mastodon_count()
        print("percentage of the post with political related:", total_count/total)
        print("percentage of the user talk about political related topics",len(mastodon_user)/mastodon_user_total())
        mastodon_percentage['post'] = total_count
        mastodon_percentage['username'] = len(mastodon_user)/mastodon_user_total()
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_percentage)


        # words frequency in mastodon 
        mastodon_words = mastodon_word_map()
        print("the mastodon words dict", mastodon_words)
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_words)

        
        time.sleep(1)
