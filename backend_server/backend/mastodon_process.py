import couchdb
import requests
import json
import time
import datetime
import itertools

#host_ip = "192.168.1.116" # Note: if running locally, use the host machine IP
#host_ip = "172.26.132.19"
host_ip = "172.26.129.100" # replalce this with instance IP the server Running

# Get today's date
today = datetime.date.today()

# Format the date as a string in the desired format
date_string = today.strftime("%Y-%m-%d")

# Combine the date string with the CouchDB name prefix
db_name = "mastodon_policy_" + date_string

couch = couchdb.Server(f'http://admin:admin@{host_ip}:5984')
# db = couch['mastodon_policy']
db = couch[db_name]

def check_date_change():
    global today
    global date_string
    global db_name
    global db

    current_date = datetime.date.today()
    if current_date != today:
        today = current_date
        date_string = today.strftime("%Y-%m-%d")
        db_name = "mastodon_policy_" + date_string
        db = couch[db_name]

def mastodon_total_count(db, db_name):
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
    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/policy_view/_view/policy_count?reduce=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true"
    response = requests.get(url)
    data = json.loads(response.text)
    count = data['rows'][0]['value']
    return count

def mastodon_count(db, db_name):
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

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/policy_view/_view/total?reduce=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true"
    response = requests.get(url)
    data = json.loads(response.text)
    count = data['rows'][0]['value']
    return count

def mastodon_user_count(db, db_name):
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
    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/policy_view/_view/user_count?group=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true"
    response = requests.get(url)
    data = json.loads(response.text)
    user_dict = dict()
    for row in data['rows']:
        user_dict[row["key"]] = row["value"]
    sorted_user_dict = dict(sorted(user_dict.items(), key=lambda item: item[1], reverse=True))

    return sorted_user_dict

def mastodon_user_total(db, db_name):
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
    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/policy_view/_view/user_total?reduce=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true"
    response = requests.get(url)
    data = json.loads(response.text)
    count = data['rows'][0]['value']

    return count

def mastodon_word_map(db, db_name):
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

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/policy_view/_view/word_count?group=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?group=true"
    response = requests.get(url)
    data = json.loads(response.text)
    word_dict = dict()
    for row in data["rows"]:
        if row["key"] not in word_dict:
            word_dict[row["key"]] = row["value"]
    word_sort_dict = dict(sorted(word_dict.items(), key=lambda item: item[1], reverse=True))
    return word_sort_dict


def get_latest_post():
    map_function = """
    function (doc) {
        emit(doc.created_at, doc);
    }
    """

    view_name = "latest_post"
    design_doc_name = "_design/post_view"

    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,
            "views": {
                view_name: {
                    "map": map_function
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/post_view/_view/latest_post?descending=true&limit=1'
    response = requests.get(url)
    data = json.loads(response.text)
    latest_post = data['rows'][0]['value'] if data['rows'] else None
    return latest_post

mastodon_data = {'host': host_ip, 'date': date_string, 'count': 0, 'total_post':0, 'post_ratio': 0, 'user_ratio':0, 'latest_post': {}}
mastodon_map = {"usermap": {}, "wordmap":{}}
if __name__ == '__main__':
    time.sleep(1)
    while True:
        # Check if the date has changed
        check_date_change()

        mastodon_data['date'] = date_string

        # number of post with related to the political related topics
        total_count  = mastodon_total_count(db, db_name)
        print("Number of policy related topic post in mastodon:", total_count)
        mastodon_data['count'] = total_count

        # number of users that post include the political related topics
        mastodon_user = mastodon_user_count(db, db_name)
        #print("Number of post for each unique user:", mastodon_user)
        mastodon_map["usermap"] = dict(itertools.islice(mastodon_user.items(), 10))

        # the percentage that include the post the political related topics and the username
        total  = mastodon_count(db, db_name)
        print('total number of mastodon post:', total)
        print("percentage of the post with political related:", total_count/total)
        print("percentage of the user talk about political related topics",len(mastodon_user)/mastodon_user_total(db, db_name))
        mastodon_data['post_ratio'] = total_count/total
        mastodon_data['user_ratio'] = len(mastodon_user)/mastodon_user_total(db, db_name)
        mastodon_data['total_post'] = total

        mastodon_data['latest_post'] = get_latest_post()

        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_data)
        #requests.post(f'http://192.168.1.116:8000/update_mastodon', json=mastodon_data)

        # words frequency in mastodon
        mastodon_words = mastodon_word_map(db, db_name)
        #print("the mastodon words dict", mastodon_words)
        mastodon_map["wordmap"] = dict(itertools.islice(mastodon_words.items(), 10))
        print(mastodon_data)

        requests.post(f'http://{host_ip}:8000/update_mastodon_map', json=mastodon_map)
        #requests.post(f'http://192.168.1.116:8000/update_mastodon', json=mastodon_data)


        time.sleep(1)
